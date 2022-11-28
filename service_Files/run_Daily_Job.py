from datetime import date, datetime
import json

def main():
    todays_date = datetime.today().strftime('%m/%d/%Y')
    print(todays_date)
    if todays_date == read_json():
        return True
    else:
        write_json()

def read_json():
    with open('./service_Files/daily_request_check.json', 'r') as rf:
        rd_json = json.load(rf)
        get_run_date = rd_json['last_run_date']
        rf.close()
    return get_run_date

def write_json():
    todays_date = datetime.today().strftime('%m/%d/%Y')
    with open('./service_Files/daily_request_check.json','r+') as rf:
        rd_json = json.load(rf)
        if rd_json['last_run_date'] != todays_date:
            rd_json['last_run_date'] = todays_date
        rf.write(json.dumps(rd_json['last_run_date']))
        rf.close()


if __name__ == '__main__':
    main()