from odoo import api, fields, models


class EduCommissionLineWizard(models.TransientModel):
    _name = "edu.commission.line.wizard"
    _description = "Wizard which represent the students list that gonna be part of the commission"

    wizard_id = fields.Many2one(comodel_name="edu.commission.wizard")
    student_id = fields.Many2one(
        string="Alumno",
        comodel_name="edu.student"
    )
    is_part = fields.Boolean(
        string="Forma parte",
        compute="_compute_is_part",
        store=True,
        readonly=False,
        precompute=True
    )

    @api.depends("wizard_id.single_commission")
    def _compute_is_part(self):
        for rec in self:
            if rec.wizard_id:
                rec.is_part = rec.wizard_id.single_commission
            else:
                rec.is_part = False
