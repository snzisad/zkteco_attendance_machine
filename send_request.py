# Documentation
# https://github.com/fananimi/pyzk 
# pip install pyzk

from zk import ZK, const
import requests
import json
ip_address = '192.168.1.201'
conn = None
url = "http://172.105.56.241:1236/attendance/dump-attendance-data"

def get_attendance_record():
    attendances = conn.get_attendance()
    
    # get and parse attendances
    # get separate date time
    # get unique user_id and date
    records = []
    date_list = []
    uid_list = []

    for single_attendance in attendances:
        date = str(single_attendance.timestamp.date())
        time = str(single_attendance.timestamp.time())
        uid = single_attendance.user_id

        single_record = {
            "date":date,
            "uid":uid,
            "time":time
        }
        records.append(single_record)

        if date not in date_list:
            date_list.append(date)

        if uid not in uid_list:
            uid_list.append(uid)

    # make separate time list for each date and user

    time_list = [[None]*len(uid_list)]*len(date_list)
    for record in records:
        date_pos = date_list.index(record['date'])
        uid_pos = uid_list.index(record['uid'])
        previous_times = time_list[date_pos][uid_pos]

        if previous_times is not None:
            previous_times.append(record['time'])
        else:
            previous_times = [record['time']]

        time_list[date_pos][uid_pos] = previous_times

    # format the data according to api
    formatted_date = {}
    for i in range(0, len(date_list)):
        user_attendance_data = {}
        for j in range(0, len(uid_list)):

            if time_list[i][j] is not None:
                uid = uid_list[j]
                times = ','.join(map(str, time_list[i][j]))
                user_attendance_data[uid]=times

        formatted_date[date_list[i]]=user_attendance_data

    # send to server
    send_to_server(formatted_date)


def send_to_server(data):
    payload = json.dumps(data)
    headers = {
      'secret-key': 'OMS11235FIBTEST',
      'Content-Type': 'application/json'
    }
     
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.status_code)
    # print(response)

    if response.json()["message"] == 1:
        conn.clear_attendance()
        print("Data successfully sent")
    else:
        print(response.json()["message"])


zk = ZK(ip_address, port=4370, timeout=5)
try:
    print('Connecting to device ...')
    conn = zk.connect()
    print('Disabling device ...')
    conn.disable_device()

    get_attendance_record()

except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
