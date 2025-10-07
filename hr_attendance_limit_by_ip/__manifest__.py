{
    "name": "Restrict Attendance By IP",
    "version": "16.0.0.0.0",
    "author": "Comunitea",
    "website": "https://www.comunitea.com",
    "category": "Human Resources",
    "description": """Use list of ips to restrict attendance registrations.""",
    "depends": [
        "base",
        "partner_firstname",
        "hr_attendance",
        "hr_attendance_report",
        'partner_external_map',
        'base_geolocalize',
    ],
    "data": [
        "views/res_users.xml",
        "views/res_config_settings.xml",
        "views/hr_employee.xml",
    ],
    "installable": True,
}
