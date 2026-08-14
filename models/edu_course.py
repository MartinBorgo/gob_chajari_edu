from odoo import fields, models


class EduCourse(models.Model):
    _name = "edu.course"
    _description = "Courses"

    name = fields.Char(
        string="Nombre del curso",
        required=True
    )
    content = fields.Html(string="Programa de contenidos")
    student_limit = fields.Integer(
        string="Cupo",
        default=15,
        required=True
    )
    teacher_ids = fields.Many2many(
        string="Profesor/es",
        comodel_name="res.users",
        relation="course_teacher_rel",
        column1="course_id",
        column2="teacher_id",
        required=True
    )
    course_instance_ids = fields.One2many(
        string="Instancias impartidas",
        comodel_name="edu.course.instance",
        inverse_name="course_id",
    )
