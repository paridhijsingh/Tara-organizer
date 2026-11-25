# test_job_status.py — Tests for job_status, with fake text only.

from job_status import classify_job_email, classify_job_type


def test_rejection():
    assert classify_job_email("We regret to inform you") == "Not moving forward"
    assert classify_job_email("We have decided to move forward with other candidates") == "Not moving forward"


def test_active():
    assert classify_job_email("Thank you for applying, we will reach out shortly") == "Active"


def test_inactive():
    assert classify_job_email("This job has expired") == "Inactive"


def test_unsure():
    assert classify_job_email("Update on your application") == "Unsure"


def test_job_type():
    assert classify_job_type("Software Engineer Intern") == "Intern"
    assert classify_job_type("Full-Time Engineer") == "Full-time"
    assert classify_job_type("AI Engineer") == ""

def test_job_alert():
    assert classify_job_email("Robert Half IS INTERESTED in seeing your application, from info@match.careerconnects.com") == "Job alert"
    assert classify_job_email("HELP WANTED: San Ramon, CA @Robert Half, from info@alerts.myjobhelper.com") == "Job alert"