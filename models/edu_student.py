from odoo import fields, models


class EduStudent(models.Model):
    _name = "edu.student"
    _description = "Students"

    name = fields.Char(
        string="Nombre completo",
        required=True
    )
    photo = fields.Binary(string="Foto")
    dni = fields.Char(
        string="DNI",
        required=True
    )
    birthday = fields.Date(
        string="Fecha de nacimiento",
        required=True
    )
    living_place = fields.Char(string="Domicilio")
    phone = fields.Char(string="Número de teléfono") 
    student_history_ids = fields.One2many(
        string="Cursos realizados",
        comodel_name="edu.student.history",
        inverse_name="student_id"
    )
    class_assistance_ids = fields.One2many(
        string="Asistencias a las clases",
        comodel_name="edu.class.assistance",
        inverse_name="student_id"
    )
