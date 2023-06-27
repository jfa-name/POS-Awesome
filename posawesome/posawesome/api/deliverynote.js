// Copyright (c) 2023 Felipe Acosta and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Note', {
    setup: function (frm) {
        frm.set_query("posa_delivery_charges", function (doc) {
            return {
                filters: { 'company': doc.company, 'disabled': 0 }
            };
        });
    },
});
