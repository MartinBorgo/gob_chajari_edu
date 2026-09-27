from odoo import api, fields, models
from odoo.tools import format_date


class EduClass(models.Model):
    _name = "edu.class"
    _description = "Courses Classes"

    name = fields.Char(
        string="Clase",
        compute="_compute_class_name",
        store=True
    )
    date = fields.Date(
        string="Fecha",
        default=fields.Date.today
    )
    teacher_id = fields.Many2one(
        string="Profesor",
        comodel_name="res.users"
    ) 
    observation = fields.Text(string="Aclaración")
    course_instance_id = fields.Many2one(
        string="Curso",
        comodel_name="edu.course.instance"
    )
    commission_id = fields.Many2one(
        string="Comisión",
        comodel_name="edu.course.commission",
        domain="[('course_instance_id', '=', course_instance_id)]"
    )
    assistance_ids = fields.One2many(
        string="Asistencias",
        comodel_name="edu.class.assistance",
        inverse_name="class_id"
    )
   
    @api.depends("date")
    def _compute_class_name(self):
        for rec in self:
            formated_date = format_date(
                self.env, rec.date, lang_code=self.env.user.lang
            )
            rec.name = f"Clase - {formated_date}"
