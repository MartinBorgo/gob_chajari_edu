from odoo import api, fields, models
from odoo.tools import format_date


class EduAttendanceWizard(models.TransientModel):
    _name = "edu.attendance.wizard"
    _description = "Wizards which generate assistance records"

    name = fields.Char(
        compute="_compute_name"
    )
    course_instance_id = fields.Many2one(
        string="Curso",
        comodel_name="edu.course.instance"
    )
    commission_id = fields.Many2one(
        string="Comisión",
        comodel_name="edu.course.commission",
        domain="[('course_instance_id', '=', course_instance_id)]",
        required=True
    )
    date = fields.Date(
        string="Fecha de la clase",
        default=fields.Date.today
    )
    line_ids = fields.One2many(
        string="Asistencias",
        comodel_name="edu.attendance.line.wizard",
        inverse_name="wizard_id",
    )

    @api.onchange("commission_id")
    def _onchange_commission_id(self):
        if not self.commission_id:
            self.line_ids = [(5, 0, 0)]
            return

        lines = [
            (0, 0, {"student_id": student.id, "assistance": True})
            for student in self.commission_id.student_ids
        ]

        self.line_ids = [(5, 0, 0)] + lines

    @api.depends("date")
    def _compute_name(self):
        for rec in self:
            if rec.date:
                formated_date = format_date(
                    self.env, rec.date, lang_code=self.env.user.lang
                ) 
                rec.name = f"Clase - {formated_date}"
            else:
                rec.name = "Nueva clase"
        
    def action_confirm(self):
        self.ensure_one()

        new_class = self.env["edu.class"].create({
            "date": self.date,
            "course_instance_id": self.course_instance_id.id,
            "commission_id": self.commission_id.id
        })

        assistances = []
        for line in self.line_ids:
            assistances.append({
                "class_id": new_class.id,
                "student_id": line.student_id.id,
                "assistance": line.assistance
            })

        if assistances:
            self.env["edu.class.assistance"].create(assistances)

        return {"type": "ir.actions.act_window_close"}
