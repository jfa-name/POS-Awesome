# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = "7.0.0"

try:
    import frappe
except ImportError:
    frappe = None

def console(*data):
    if frappe:
        frappe.publish_realtime("toconsole", data, user=frappe.session.user)
