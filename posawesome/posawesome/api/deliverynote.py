# -*- coding: utf-8 -*-
# Copyright (c) 2023, Felipe Acosta and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, add_days
from posawesome.posawesome.doctype.pos_coupon.pos_coupon import update_coupon_code_count
from posawesome.posawesome.api.posapp import get_company_domain
from posawesome.posawesome.doctype.delivery_charges.delivery_charges import (
    get_applicable_delivery_charges,
)


def validate(doc, method):
    set_patient(doc)
    auto_set_delivery_charges(doc)
    calc_delivery_charges(doc)


def before_submit(doc, method):
    add_loyalty_point(doc)
    create_deliverynote(doc)
    update_coupon(doc, "used")


def before_cancel(doc, method):
    update_coupon(doc, "cancelled")


def add_loyalty_point(deliverynote_doc):
    # Guard: posa_offers custom field may not exist on non-POS delivery notes
    posa_offers = getattr(deliverynote_doc, 'posa_offers', None) or []
    for offer in posa_offers:
        if offer.offer == "Loyalty Point":
            original_offer = frappe.get_doc("POS Offer", offer.offer_name)
            if original_offer.loyalty_points > 0:
                loyalty_program = frappe.get_value(
                    "Customer", deliverynote_doc.customer, "loyalty_program"
                )
                if not loyalty_program:
                    loyalty_program = original_offer.loyalty_program
                doc = frappe.get_doc(
                    {
                        "doctype": "Loyalty Point Entry",
                        "loyalty_program": loyalty_program,
                        "loyalty_program_tier": original_offer.name,
                        "customer": deliverynote_doc.customer,
                        "deliverynote": deliverynote_doc.name,
                        "loyalty_points": original_offer.loyalty_points,
                        "expiry_date": add_days(deliverynote_doc.posting_date, 10000),
                        "posting_date": deliverynote_doc.posting_date,
                        "company": deliverynote_doc.company,
                    }
                )
                doc.insert(ignore_permissions=True)


def create_deliverynote(doc):
    # Guard: all posa_* fields may not exist on non-POS delivery notes
    pos_profile = getattr(doc, 'pos_profile', None)
    posa_pos_opening_shift = getattr(doc, 'posa_pos_opening_shift', None)
    posa_delivery_date = getattr(doc, 'posa_delivery_date', None)
    posa_notes = getattr(doc, 'posa_notes', None)

    if not pos_profile:
        return

    if (
        posa_pos_opening_shift
        and pos_profile
        and posa_delivery_date
        and not doc.update_stock
        and frappe.get_value("POS Profile", pos_profile, "posa_allow_deliverynote")
    ):
        deliverynote_doc = make_deliverynote(doc.name)
        if deliverynote_doc:
            deliverynote_doc.posa_notes = posa_notes
            deliverynote_doc.flags.ignore_permissions = True
            deliverynote_doc.flags.ignore_account_permission = True
            deliverynote_doc.save()
            deliverynote_doc.submit()
            url = frappe.utils.get_url_to_form(
                deliverynote_doc.doctype, deliverynote_doc.name
            )
            msgprint = "Delivery Note Created at <a href='{0}'>{1}</a>".format(
                url, deliverynote_doc.name
            )
            frappe.msgprint(
                _(msgprint), title="Delivery Note Created", indicator="green", alert=True
            )
            i = 0
            for item in deliverynote_doc.items:
                doc.items[i].deliverynote = deliverynote_doc.name
                doc.items[i].so_detail = item.name
                i += 1


def make_deliverynote(source_name, target_doc=None, ignore_permissions=True):
    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.flags.ignore_permissions = ignore_permissions
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")

    def update_item(obj, target, source_parent):
        target.stock_qty = flt(obj.qty) * flt(obj.conversion_factor)
        target.delivery_date = (
            getattr(obj, 'posa_delivery_date', None)
            or getattr(source_parent, 'posa_delivery_date', None)
        )

    doclist = get_mapped_doc(
        "Delivery Note",
        source_name,
        {
            "Delivery Note": {
                "doctype": "Delivery Note",
            },
            "Delivery Note Item": {
                "doctype": "Delivery Note Item",
                "field_map": {
                    "cost_center": "cost_center",
                    "Warehouse": "warehouse",
                    "delivery_date": "posa_delivery_date",
                    "posa_notes": "posa_notes",
                },
                "postprocess": update_item,
            },
            "Sales Taxes and Charges": {
                "doctype": "Sales Taxes and Charges",
                "add_if_empty": True,
            },
            "Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
            "Payment Schedule": {"doctype": "Payment Schedule", "add_if_empty": True},
        },
        target_doc,
        set_missing_values,
        ignore_permissions=ignore_permissions,
    )

    return doclist


def update_coupon(doc, transaction_type):
    # Guard: posa_coupons custom field may not exist on non-POS delivery notes
    posa_coupons = getattr(doc, 'posa_coupons', None) or []
    for coupon in posa_coupons:
        if not coupon.applied:
            continue
        update_coupon_code_count(coupon.coupon, transaction_type)


def set_patient(doc):
    domain = get_company_domain(doc.company)
    if domain != "Healthcare":
        return
    patient_list = frappe.get_all(
        "Patient", filters={"customer": doc.customer}, page_length=1
    )
    if len(patient_list) > 0:
        doc.patient = patient_list[0].name


def auto_set_delivery_charges(doc):
    # Guard: pos_profile and posa_* fields may not exist on non-POS delivery notes
    pos_profile = getattr(doc, 'pos_profile', None)
    if not pos_profile:
        return

    if not frappe.get_cached_value(
        "POS Profile", pos_profile, "posa_auto_set_delivery_charges"
    ):
        return

    posa_delivery_charges = getattr(doc, 'posa_delivery_charges', None)
    posa_delivery_charges_rate = getattr(doc, 'posa_delivery_charges_rate', None)
    shipping_address_name = getattr(doc, 'shipping_address_name', None)

    delivery_charges = get_applicable_delivery_charges(
        doc.company,
        pos_profile,
        doc.customer,
        shipping_address_name,
        posa_delivery_charges,
        restrict=True,
    )

    if posa_delivery_charges:
        if posa_delivery_charges_rate:
            return
        else:
            if len(delivery_charges) > 0:
                doc.posa_delivery_charges_rate = delivery_charges[0].rate
    else:
        if len(delivery_charges) > 0:
            doc.posa_delivery_charges = delivery_charges[0].name
            doc.posa_delivery_charges_rate = delivery_charges[0].rate
        else:
            doc.posa_delivery_charges = None
            doc.posa_delivery_charges_rate = None


def calc_delivery_charges(doc):
    # Guard: pos_profile and posa_* fields may not exist on non-POS delivery notes
    pos_profile = getattr(doc, 'pos_profile', None)
    if not pos_profile:
        return

    posa_delivery_charges = getattr(doc, 'posa_delivery_charges', None)

    old_doc = None
    calculate_taxes_and_totals = False
    if not doc.is_new():
        old_doc = doc.get_doc_before_save()
        old_posa_delivery_charges = getattr(old_doc, 'posa_delivery_charges', None)
        if not posa_delivery_charges and not old_posa_delivery_charges:
            return
    else:
        if not posa_delivery_charges:
            return

    if not posa_delivery_charges:
        doc.posa_delivery_charges_rate = 0

    charges_doc = None
    if posa_delivery_charges:
        charges_doc = frappe.get_cached_doc(
            "Delivery Charges", posa_delivery_charges
        )
        doc.posa_delivery_charges_rate = charges_doc.default_rate
        charges_profile = next(
            (i for i in charges_doc.profiles if i.pos_profile == pos_profile), None
        )
        if charges_profile:
            doc.posa_delivery_charges_rate = charges_profile.rate

    if old_doc:
        old_posa_delivery_charges = getattr(old_doc, 'posa_delivery_charges', None)
        if old_posa_delivery_charges:
            old_charges = next(
                (
                    i
                    for i in doc.taxes
                    if i.charge_type == "Actual"
                    and i.description == old_posa_delivery_charges
                ),
                None,
            )
            if old_charges:
                doc.taxes.remove(old_charges)
                calculate_taxes_and_totals = True

    if posa_delivery_charges:
        doc.append(
            "taxes",
            {
                "charge_type": "Actual",
                "description": posa_delivery_charges,
                "tax_amount": doc.posa_delivery_charges_rate,
                "cost_center": charges_doc.cost_center,
                "account_head": charges_doc.shipping_account,
            },
        )
        calculate_taxes_and_totals = True

    if calculate_taxes_and_totals:
        doc.calculate_taxes_and_totals()