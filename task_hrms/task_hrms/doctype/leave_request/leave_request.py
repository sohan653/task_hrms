# Copyright (c) 2025, Sohanur Rahman and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.model.document import Document

class LeaveRequest(Document):

	def before_save(self):
		if self.status == "Approved":
			self.approved_by = frappe.session.user


	def validate(self):
		self.validate_date_range()
		self.validate_leave_duration()
		self.calculate_total_days()


	def validate_date_range(self):
		if self.from_date and self.to_date:
			if self.from_date > self.to_date:
				frappe.throw(_("From Date must be before To Date"))

	def validate_leave_duration(self):
		if self.from_date and self.to_date:
			total_days = self.calculate_working_days()
			if total_days == 0:
				frappe.throw(_("Leave duration cannot be 0 days."))
			if total_days > 5:
				frappe.throw(_("Leave duration cannot exceed 5 days."))

	def calculate_working_days(self):
		from_date = self.from_date
		to_date = self.to_date
		if isinstance(from_date, str):
			from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
		if isinstance(to_date, str):	
			to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
		
		total_days = 0
		current_date = from_date
		
		while current_date <= to_date:

			if current_date.weekday()!=6 and current_date.weekday()!=0:  
				total_days += 1
			current_date += timedelta(days=1)
		
		return total_days

	def calculate_total_days(self):

		if self.from_date and self.to_date:
			self.total_days = self.calculate_working_days()
