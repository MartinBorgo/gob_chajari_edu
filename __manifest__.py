{
    "name": "Gestión de cursos",
    "summary": "Una aplicación simple para la gestión de cursos.",
    "author": "Martin Borgo",
    "category": "Uncategorized",
    "application": True,
    "version": "19.0.1.0.0",
    "depends": ["base"],
    "data": [
        # Security
        "security/security.xml",
        "security/ir.model.access.csv",
        # Wizards
        "wizards/edu_attendance_wizard.xml",
        "wizards/edu_commission_wizard.xml",
        # Views
        "views/edu_season_view.xml",
        "views/edu_student_view.xml",
        "views/edu_student_history_view.xml",
        "views/edu_course_view.xml",
        "views/edu_course_instance_view.xml",
        "views/edu_course_commission_view.xml",
        "views/edu_class_view.xml",
        "views/edu_class_assistance_view.xml",
        "views/menu.xml",
    ],
    "license": "LGPL-3",
}
