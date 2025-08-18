// Copyright (c) 2025, Sohanur Rahman and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Leave Summary by Employee"] = {
	"filters": [
		{
			"fieldname": "employee",
			"label": "Employee",
			"fieldtype": "Link",
			"options": "Employee",
			"reqd": 1
		},
	]
};
