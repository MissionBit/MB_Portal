def get_generic_absence_notification(student, date):
    return (
        "Hello, our records indicate that %s %s was absent on %s, "
        "please advise." % (student.first_name, student.last_name, date)
    )
