from odoo import api, fields, models


class EduCourseInstance(models.Model):
    _name = "edu.course.instance"
    _description = "Instances of the Courses"

    name = fields.Char(
        string="Curso",
        compute="_compute_instance_name"
    )
    state = fields.Selection(
        string="Estado del curso",
        selection=[
            ("draft", "En curso"),
            ("done", "Finalizado")
        ],
        default="draft"
    )
    course_id = fields.Many2one(
        string="Curso",
        comodel_name="edu.course",
        required=True
    )
    season_id = fields.Many2one(
        string="Ciclo lectivo",
        comodel_name="edu.season",
        required=True
    )
    period = fields.Selection(
        string="Trimestre",
        selection=[
            ("first", "Primer Trimestre"),
            ("second", "Segundo Trimestre"),
            ("third", "Tercer Trimestre"),
        ],
        required=True
    )
    class_ids = fields.One2many(
        string="Clases impartidas",
        comodel_name="edu.class",
        inverse_name="course_instance_id",
    )
    student_ids = fields.Many2many(
        string="Alumnos",
        comodel_name="edu.student",
        relation="course_instance_student_rel",
        column1="course_instance_id",
        column2="student_id",
    )
    student_history_ids = fields.One2many(
        string="Notas finales",
        comodel_name="edu.student.history",
        inverse_name="course_instance_id"
    )
    commission_ids = fields.One2many(
        string="Comisiones",
        comodel_name="edu.course.commission",
        inverse_name="course_instance_id"
    )
    is_teacher = fields.Boolean(
        compute="_compute_is_theacher",
        search="_search_is_teacher"
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super(EduCourseInstance, self).create(vals_list)
        for record in records:
            if record.student_ids:
                record._update_student_history(record.student_ids.ids)

        return records

    def write(self, vals):
        res = super(EduCourseInstance, self).write(vals)

        if 'student_ids' in vals:
            for record in self:
                existing_student_ids = record.student_history_ids.mapped('student_id').ids
                new_students = record.student_ids.filtered(
                    lambda s: s.id not in existing_student_ids
                )

                if new_students:
                    record._update_student_history(new_students.ids)

        return res

    def _update_student_history(self, student_ids):
        for student_id in student_ids:
            self.env['edu.student.history'].create({
                'course_instance_id': self.id,
                'student_id': student_id,
                'student_state': 'attending',
            })

    @api.depends("course_id.name", "season_id.name", "period")
    def _compute_instance_name(self):
        selection_dict = dict(self._fields['period'].selection)
        for rec in self:
            if rec.course_id and rec.season_id and rec.period:
                period_label = selection_dict.get(rec.period)
                rec.name = f"{rec.course_id.name} - {period_label} - {rec.season_id.name}"
            else:
                rec.name = "Nueva Instancia"

    @api.depends("course_id.teacher_ids")
    def _compute_is_theacher(self):
        for rec in self:
            rec.is_teacher = self.env.user in rec.course_id.teacher_ids

    def _search_is_teacher(self, operator, value):
        return [("course_id.teacher_ids", "in", [self.env.user.id])]
