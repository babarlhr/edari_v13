# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.misc import str2bool, xlwt
import io
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class HREmployeeReportWizardNew(models.TransientModel):
    _name = "hr.employee.report.wizard.new"

    employee_ids = fields.Many2many('hr.employee', string='Employees')

    def add_header_label(self, worksheet, style, row, col):
        worksheet.write(row, col, "S.No", style)
        worksheet.write(row, col + 1, "Employee Name", style)
        worksheet.write(row, col + 2, "ID Number", style)
        worksheet.write(row, col + 3, "Operating Unit", style)
        worksheet.write(row, col + 4, "Department", style)
        worksheet.write(row, col + 5, "Job Position", style)
        worksheet.write(row, col + 6, "Line Manager", style)
        worksheet.write(row, col + 7, "Senior Manager", style)
        worksheet.write(row, col + 8, "Primary Mobile Number", style)

    def generate_hr_employee_report(self):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("Employees")
        style = xlwt.easyxf(
            "font: bold True;"
            "align: vert centre, horiz center;"
            "border: right 2, left 2, top 2, bottom 2;"
        )
        style_date = xlwt.XFStyle()
        style_date.num_format_str = DF
        
        row, col = 0, 0
        self.add_header_label(worksheet, style, row, col)

        row = 1
        i = 0
        for emp in self.employee_ids:
            col = 0
            i += 1
            s_no = i
            name = emp.name
            id_number = emp.identification_id if emp.identification_id else ""
            operating_unit = emp.operating_unit_id.name if emp.operating_unit_id else ""
            department = emp.department_id.name if emp.department_id else ""
            job_position = emp.job_id.name if emp.job_id else ""
            line_manager = emp.line_manager.name if emp.line_manager else ""
            senior_manager = emp.senior_manager.name if emp.senior_manager else ""
            phone = emp.work_phone if emp.work_phone else ""

            worksheet.write(row, col, s_no)
            worksheet.write(row, col + 1, name)
            worksheet.write(row, col + 2, id_number)
            worksheet.write(row, col + 3, operating_unit)
            worksheet.write(row, col + 4, department)
            worksheet.write(row, col + 5, job_position)
            worksheet.write(row, col + 6, line_manager)
            worksheet.write(row, col + 7, senior_manager)
            worksheet.write(row, col + 8, phone)
            row += 1
        fp = io.BytesIO()
        workbook.save(fp)
        filename = "employees_report.xls"
        export_id = self.env["hr.employee.report"].create(
            {"excel_file": base64.encodestring(fp.getvalue()), "file_name": filename}
        )
        fp.close()
        return {
            "view_mode": "form",
            "res_id": export_id.id,
            "res_model": "hr.employee.report",
            "view_type": "form",
            "type": "ir.actions.act_window",
            "context": self._context,
            "target": "new",
        }


class HREmployeeReport(models.TransientModel):
    _name = "hr.employee.report"

    excel_file = fields.Binary("Report file")
    file_name = fields.Char("Excel File", size=64)
