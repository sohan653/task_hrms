# Copyright (c) 2025, Sohanur Rahman and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    columns = [
        {
            "fieldname": "employee",
            "label": _("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "width": 200
        },
        {
            "fieldname": "total_leave_requests",
            "label": _("Total Leave Requests"),
            "fieldtype": "Int",
            "width": 200
        },
        {
            "fieldname": "approved_requests",
            "label": _("Approved Requests"),
            "fieldtype": "Int",
            "width": 200
        },
        {
            "fieldname": "rejected_requests",
            "label": _("Rejected Requests"),
            "fieldtype": "Int",
            "width": 200
        }
    ]
    return columns

def get_data(filters=None):
    query = """
        SELECT 
            lr.employee,
            COUNT(*) as total_leave_requests,
            SUM(CASE 
                WHEN lr.status = 'Approved' OR lr.workflow_state = 'Approved' 
                THEN 1 
                ELSE 0 
            END) as approved_requests,
            SUM(CASE 
                WHEN lr.status = 'Rejected' OR lr.workflow_state = 'Rejected' 
                THEN 1 
                ELSE 0 
            END) as rejected_requests
        FROM 
            `tabLeave Request`  lr
        WHERE 
           lr.docstatus != 2
    """
    
    conditions = []
    values = []
    
    if filters:
        if filters.get("employee"):
            conditions.append("lr.employee = %s")
            values.append(filters.get("employee"))

    if conditions:
        query += " AND " + " AND ".join(conditions)
    
    query += " GROUP BY lr.employee"
    
    data = frappe.db.sql(query, values, as_dict=True)
    
    return data