// Copyright (c) 2025, Sohanur Rahman and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Request', {
	refresh: function(frm) {

	},
	leave_type: function(frm) {
        if (frm.doc.leave_type === 'EL') {
			frm.set_value("leave_type", "")
            frappe.msgprint({
                title: __('Information'),
                message: __('Earned Leave requires manager approval.'),
                indicator: 'blue'
            });
        }
    },
	from_date: function(frm) {
		calculate_total_days(frm);
	},
	to_date: function(frm) {
		calculate_total_days(frm);
	},
	// validate: function(frm) {
	// 	if (frm.doc.status === 'Approved') {
	// 		frm.set_value("approved_by", frappe.session.user)
	// 	}
	// }
});



function calculate_total_days(frm) {
    if (frm.doc.from_date && frm.doc.to_date) {
        let from_date = frappe.datetime.str_to_obj(frm.doc.from_date);
        let to_date = frappe.datetime.str_to_obj(frm.doc.to_date);
        
 
        if (from_date > to_date) {
			frm.set_value("from_date", "")
			frm.set_value("to_date", "")
            frappe.msgprint({
                title: __('Invalid Date Range'),
                message: __('From Date must be before To Date'),
                indicator: 'red'
            });
            return;
        }
        let total_days = 0;
        let current_date = new Date(from_date);
        
        while (current_date <= to_date) {
            let day_of_week = current_date.getDay();

            if (day_of_week !== 0 && day_of_week !== 6) {
                total_days++;
            }
            current_date.setDate(current_date.getDate() + 1);
        }
        frm.set_value('total_days', total_days);
		frm.refresh_fields('total_days');
        
    }
}
