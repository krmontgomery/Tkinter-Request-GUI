from app_service_files.check_last_run_date import main
from app_service_files.daily_Request_Query import startup_Request_Due_Date_Alert
from app_service_files.send_reminder_email import daily_request_check

def run_daily_job_main():
    records = []

    if main() == True:
        pass
    else:
        for item in startup_Request_Due_Date_Alert():
            records.append(list(item))
        daily_request_check(records)