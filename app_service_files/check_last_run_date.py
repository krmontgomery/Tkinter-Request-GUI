from datetime import datetime
import json

def main():
    todays_date = datetime.today().strftime('%m/%d/%Y')
    json_object = read_json()
    last_date = json_object['last_run_date']
    if todays_date == last_date:
        return True
    else:
        write_json(json_object)
        return False

def read_json():
    with open('app_service_files/dailyRequestCheck.json', 'r') as rf:
        rd_json = json.load(rf)
        rf.close()
    return rd_json

def write_json(object):
    todays_date = datetime.today().strftime('%m/%d/%Y')
    json_object = object
    json_object['last_run_date'] = todays_date
    with open('app_service_files/dailyRequestCheck.json','w') as wf:
        json.dump(json_object, wf)
        wf.close()

# if __name__ == '__main__':
#     main()