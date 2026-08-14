from odoo import api ,fields, models
from odoo.exceptions import UserError


class EduCommissionWizard(models.TransientModel):
    _name = "edu.commission.wizard"
    _description = "Wizard which create course commissions"

    name = fields.Char(
        string="Comisión",
        required=True
    )
    single_commission = fields.Boolean(string="Comisión única")
    class_days = fields.Selection(
        string="Día de cursada",
        selection=[
            ("mon", "Lunes"),
            ("tue", "Martes"),
            ("wed", "Miercoles"),
            ("thu", "Jueves"),
            ("fri", "Viernes"),
        ],
        required=True
    )
    start_hour = fields.Float(
        string="Hora de inicio",
        required=True
    )
    end_hour = fields.Float(
        string="Hora de finalización",
        required=True
    )
    course_instance_id = fields.Many2one(
        string="Curso",
        comodel_name="edu.course.instance"
    )
    line_ids = fields.One2many(
        string="Alumnos",
        comodel_name="edu.commission.line.wizard",
        inverse_name="wizard_id",
        compute="_compute_line_ids",
        store=True,
        precompute=True,
        readonly=False
    )

    @api.depends("course_instance_id")
    def _compute_line_ids(self):
        for rec in self:
            course = rec.course_instance_id
            assigned_students = course.commission_ids.mapped("student_ids")
            available_students = course.student_ids - assigned_students
            rec.line_ids = [
                fields.Command.create({"student_id": student.id, "is_part": False})
                for student in available_students
            ]
      
    def action_confirm(self):
        selected_students = self.line_ids.filtered(lambda l: l.is_part).mapped("student_id")

        if not selected_students:
            raise UserError("Debe seleccionar al menos un alumno para poder crear la comisión.")

        if self.start_hour >= self.end_hour:
            raise UserError("La hora de inicio de clases no puede ser mayor o igual a la hora de finalización.")

        self.env["edu.course.commission"].create({
            "name": self.name,
            "class_days": self.class_days,
            "start_hour": self.start_hour,
            "end_hour": self.end_hour,
            "course_instance_id": self.course_instance_id.id,
            "student_ids": [(6, 0, selected_students.ids)],
        })

        return {"type": "ir.actions.act_window_close"}
