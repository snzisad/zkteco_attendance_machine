# documentation
# https://github.com/fananimi/pyzk 
# pip install pyzk

from zk import ZK, const
ip_address = '192.168.1.201'
conn = None


def users_list():
    users = conn.get_users()
    for user in users:
    	print_user_info(user)
    	

def print_user_info(user):
    privilege = 'User'
    if user.privilege == const.USER_ADMIN:
        privilege = 'Admin'

    print('  UID 		: #{}'.format(user.uid))
    print('  Name       : {}'.format(user.name))
    print('  Privilege  : {}'.format(privilege))
    print('  Password   : {}'.format(user.password))
    print('  Group ID   : {}'.format(user.group_id))
    print('  User  ID   : {}'.format(user.user_id))


def add_edit_user(uid, name, privilege, password, group_id, user_id, card):
	conn.set_user(
		uid = uid,
		name=name, 
		privilege=privilege, 
		password=password, 
		group_id=group_id, 
		user_id=user_id, 
		card=card
	)

	print("User saved successfully")


def remove_user(uid):
	conn.delete_user(uid=uid)
	print("User deleted successfully")

def get_attendance_record():
    # Get attendances (will return list of Attendance object)
    attendances = conn.get_attendance()
    for single_attendance in attendances:
    	print_attendance_data(single_attendance)

def print_attendance_data(single_attendance):
    print('  User  ID   : {}'.format(single_attendance.user_id))
    print('  Time  : {}'.format(single_attendance.timestamp))
    print('  Status   : {}'.format(single_attendance.status))
    print('  Punch   : {}'.format(single_attendance.punch))


def clear_attendance_record():
    # Clear attendances records
    conn.clear_attendance()


def clear_all_date():
    # DANGER!!! This command will be erase all data in the device (incuded: user, attendance report, and finger database)
    conn.clear_data()
    print("Removed all data")

def clear_buffer_data():
    # clear buffer
    conn.free_data()
    print("Buffer cleared")

def poweroff():
    # shutdown connected device
    conn.poweroff()
    print("Device turned off")
       
def restart():
    # restart connected device
    conn.restart()
    print("Device restarted")
       

def get_set_time():
    from datetime import datetime
    # get current machine's time
    zktime = conn.get_time()
    print(zktime)
    # update new time to machine
    newtime = datetime.today()
    conn.set_time(newtime)

def device_information():
    print("Firmware Version: "+str(conn.get_firmware_version()))
    print("Serial Number: "+str(conn.get_serialnumber()))
    print("Platform: "+str(conn.get_platform()))
    print("Device Name: "+str(conn.get_device_name()))
    print("Face Version: "+str(conn.get_face_version()))
    print("Fingerprint Version: "+str(conn.get_fp_version()))
    print("Extend FMT: "+str(conn.get_extend_fmt()))
    print("User Extend FMT: "+str(conn.get_user_extend_fmt()))
    print("Face Function On: "+str(conn.get_face_fun_on()))
    print("Compact Old Firmware: "+str(conn.get_compat_old_firmware()))
    print("Network Parameters: "+str(conn.get_network_params()))
    print("MAC Address: "+str(conn.get_mac()))
    print("Pin Width: "+str(conn.get_pin_width()))

       
def device_usage_options():
    print("Total Users: "+str(conn.users))
    print("Total Fingers: "+str(conn.fingers))
    print("Total Attendance Records: "+str(conn.records))
    print("Total Users Capacity: "+str(conn.users_cap))
    print("Total Fingers Capacity: "+str(conn.fingers_cap))


def live_attendance():
    # live capture! (timeout at 10s)
    for attendance in conn.live_capture():
        if attendance is None:
            # implement here timeout logic
            print("Timeout")

        else:
        	print_attendance_data(attendance)

        #if you need to break gracefully just set
        #   conn.end_live_capture = True
        #
        # On interactive mode,
        # use Ctrl+C to break gracefully
        # this way it restores timeout
        # and disables live capture



def perform_operations():
	# users_list()
 #    add_edit_user(
 #    	uid = 17,
 #    	name = "Ikram Khan Xohan",
 #    	password = "123456",
 #    	privilege = const.USER_DEFAULT, # const.USER_DEFAULT, const.USER_ADMIN
 #    	group_id = "",
 #    	user_id = "17",
 #    	card = 0,
	# )
	# remove_user(121)
	get_attendance_record()
	# clear_attendance_record()
	# clear_all_date()
	# clear_buffer_data()
	# poweroff()
	# restart()
	# live_attendance()
	# get_set_time()
	# device_information()
	# device_usage_options()


zk = ZK(ip_address, port=4370, timeout=5)
try:
    print('Connecting to device ...')
    conn = zk.connect()
    print('Disabling device ...')
    conn.disable_device()

    perform_operations()

except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()


