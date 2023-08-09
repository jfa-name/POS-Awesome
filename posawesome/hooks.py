# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "posawesome"
app_title = "POS Awesome"
app_publisher = "Youssef Restom"
app_description = "POS Awesome"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "youssef@totrox.com"
app_license = "GPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/posawesome/css/posawesome.css"
# app_include_js = "/assets/posawesome/js/posawesome.js"
app_include_js = [
    "/assets/posawesome/node_modules/vuetify/dist/vuetify.js",
    "posawesome.bundle.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/posawesome/css/posawesome.css"
# web_include_js = "/assets/posawesome/js/posawesome.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "POS Profile": "posawesome/api/pos_profile.js",
    "Sales Invoice": "posawesome/api/invoice.js",
    "Delivery Note": "posawesome/api/deliverynote.js",
    "Company": "posawesome/api/company.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "posawesome.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "posawesome.install.before_install"
# after_install = "posawesome.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "posawesome.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Invoice": {
        "validate": "posawesome.posawesome.api.invoice.validate",
        "before_submit": "posawesome.posawesome.api.invoice.before_submit",
        "before_cancel": "posawesome.posawesome.api.invoice.before_cancel",
    },
    "Delivery Note": {
        "validate": "posawesome.posawesome.api.deliverynote.validate",
        "before_submit": "posawesome.posawesome.api.deliverynote.before_submit",
        "before_cancel": "posawesome.posawesome.api.deliverynote.before_cancel",
    },
    "Customer": {
        "validate": "posawesome.posawesome.api.customer.validate",
        "after_insert": "posawesome.posawesome.api.customer.after_insert",
    },
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"posawesome.tasks.all"
# 	],
# 	"daily": [
# 		"posawesome.tasks.daily"
# 	],
# 	"hourly": [
# 		"posawesome.tasks.hourly"
# 	],
# 	"weekly": [
# 		"posawesome.tasks.weekly"
# 	]
# 	"monthly": [
# 		"posawesome.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "posawesome.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "posawesome.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "posawesome.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                (
                    "Sales Invoice-posa_pos_opening_shift",
                    "Sales Invoice-posa_is_printed",
                    "Sales Invoice-posa_offers",
                    "Sales Invoice-posa_coupons",
                    "Sales Invoice-posa_additional_notes_section",
                    "Sales Invoice-posa_notes",
                    "Sales Invoice-posa_column_break_111",
                    "Sales Invoice-posa_delivery_date",
                    "Sales Invoice-posa_delivery_charges",
                    "Sales Invoice-posa_delivery_charges_rate",
                    "Sales Invoice Item-posa_offers",
                    "Sales Invoice Item-posa_row_id",
                    "Sales Invoice Item-posa_offer_applied",
                    "Sales Invoice Item-posa_is_offer",
                    "Sales Invoice Item-posa_is_replace",
                    "Sales Invoice Item-posa_notes",
                    "Sales Invoice Item-posa_delivery_date",
                    "Item Barcode-posa_uom",
                    "POS Profile-posa_pos_awesome_settings",
                    "POS Profile-posa_allow_delete",
                    "POS Profile-posa_allow_user_to_edit_rate",
                    "POS Profile-posa_allow_user_to_edit_additional_discount",
                    "POS Profile-posa_allow_user_to_edit_item_discount",
                    "POS Profile-posa_display_items_in_stock",
                    "POS Profile-posa_allow_submissions_in_background_job",
                    "POS Profile-posa_allow_partial_payment",
                    "POS Profile-posa_allow_credit_sale",
                    "POS Profile-posa_pos_awesome_advance_settings",
                    "POS Profile-posa_max_discount_allowed",
                    "POS Profile-posa_allow_return",
                    "POS Profile-posa_col_1",
                    "POS Profile-posa_scale_barcode_start",
                    "POS Profile-posa_local_storage",
                    "POS Profile-posa_cash_mode_of_payment",
                    "POS Profile-use_cashback",
                    "POS Profile-use_customer_credit",
                    "POS Profile-posa_hide_closing_shift",
                    "POS Profile-posa_apply_customer_discount",
                    "POS Profile-posa_auto_set_batch",
                    "POS Profile-posa_search_serial_no",
                    "POS Profile-posa_allow_sales_order",
                    "POS Profile-posa_column_break_112",
                    "POS Profile-posa_allow_delivery_note",
                    "POS Profile-posa_show_template_items",
                    "POS Profile-posa_hide_variants_items",
                    "POS Profile-posa_fetch_coupon",
                    "POS Profile-posa_tax_inclusive",
                    "POS Profile-posa_use_percentage_discount",
                    "POS Profile-posa_allow_customer_purchase_order",
                    "POS Profile-posa_allow_print_last_invoice",
                    "POS Profile-posa_display_additional_notes",
                    "POS Profile-posa_allow_write_off_change",
                    "POS Profile-posa_new_line",
                    "POS Profile-posa_input_qty",
                    "POS Profile-posa_display_item_code",
                    "POS Profile-posa_allow_zero_rated_items",
                    "POS Profile-posa_allow_print_draft_invoices",
                    "POS Profile-posa_auto_set_delivery_charges",
                    "POS Profile-posa_use_delivery_charges",
                    "POS Profile-hide_expected_amount",
                    "POS Profile-posa_allow_change_posting_date",
                    "POS Profile-posa_default_card_view",
                    "POS Profile-posa_default_sales_order",
                    "POS Profile-column_break_dqsba",
                    "POS Profile-posa_use_server_cache",
                    "POS Profile-posa_server_cache_duration",
                    "POS Profile-posa_allow_duplicate_customer_names",
                    "POS Profile-column_break_anyol",
                    "POS Profile-pose_use_limit_search",
                    "POS Profile-posa_search_limit",
                    "POS Profile-posa_search_batch_no",
                    "POS Profile-pos_awesome_payments",
                    "POS Profile-posa_use_pos_awesome_payments",
                    "POS Profile-posa_allow_make_new_payments",
                    "POS Profile-posa_allow_reconcile_payments",
                    "POS Profile-column_break_uolvm",
                    "POS Profile-posa_allow_mpesa_reconcile_payments",
                    "POS Profile-posa_allow_print_draft_deliverynotes",
                    "POS Profile-posa_default_delivery_note",
                    "POS Profile-print_format_for_online",
                    "POS Profile-posa_allow_delivery_note",
                    "Batch-posa_batch_price",
                    "Customer-posa_discount",
                    "Customer-posa_referral_code",
                    "Customer-posa_referral_company",
                    "Customer-posa_referral_section",
                    "Customer-posa_birthday",
                    "Sales Order-posa_additional_notes_section",
                    "Sales Order-posa_notes",
                    "Sales Order-posa_offers",
                    "Sales Order-posa_coupons",
                    "Sales Order Item-posa_notes",
                    "Sales Order Item-posa_row_id",
                    "Delivery Note-pos_profile",
                    "Delivery Note-loyalty_points_redemption",
                    "Delivery Note-redeem_loyalty_points",
                    "Delivery Note-loyalty_points",
                    "Delivery Note-loyalty_amount",
                    "Delivery Note-loyalty_program",
                    "Delivery Note-loyalty_redemption_account",
                    "Delivery Note-loyalty_redemption_cost_center",
                    "Delivery Note-posa_pos_opening_shift",
                    "Delivery Note-posa_additional_notes_section",
                    "Delivery Note-posa_notes",
                    "Delivery Note-posa_column_break_111",
                    "Delivery Note-posa_coupons",
                    "Delivery Note-posa_delivery_date",
                    "Delivery Note-posa_is_printed",
                    "Delivery Note-posa_offers",
                    "Delivery Note-posa_delivery_charges",
                    "Delivery Note-posa_delivery_charges_rate",
                    "Delivery Note Item-posa_offers",
                    "Delivery Note Item-posa_row_id",
                    "Delivery Note Item-posa_offer_applied",
                    "Delivery Note Item-posa_is_offer",
                    "Delivery Note Item-posa_is_replace",
                    "Delivery Note Item-posa_notes",
                    "Delivery Note Item-posa_delivery_date",
                    "Company-posa_referral_section",
                    "Company-posa_auto_referral",
                    "Company-posa_column_break_22",
                    "Company-posa_customer_offer",
                    "Company-posa_primary_offer",
                    "Company-posa_referral_campaign",
                    "Address-posa_delivery_charges",
                ),
            ]
        ],
    },
    {
        "doctype": "Property Setter",
        "filters": [["name", "in", ("Sales Invoice-posa_pos_opening_shift-no_copy")]],
    },
]
