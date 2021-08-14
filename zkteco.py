# documentation
# https://github.com/fananimi/pyzk 
# pip install pyzk

from zk import ZK, const

def users_operation():
    # Create user
    conn.set_user(
        uid=1, 
        name='Mr ABCD', 
        privilege=const.USER_ADMIN, 
        password='12345678', 
        group_id='', 
        user_id='12', 
        card=0
    )
    # Get all users (will return list of User object)
    users = conn.get_users()
    # Delete User
    conn.delete_user(uid=1)

def users_list():

    users = conn.get_users()
    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'

        print('- UID #{}'.format(user.uid))
        print('  Name       : {}'.format(user.name))
        print('  Privilege  : {}'.format(user.privilege))
        print('  Password   : {}'.format(user.password))
        print('  Group ID   : {}'.format(user.group_id))
        print('  User  ID   : {}'.format(user.user_id))


def fingerprints():
    # Get  a single Fingerprint (will return a Finger object)
    template = conn.get_user_template(uid=1, temp_id=0) #temp_id is the finger to read 0~9
    # Get all fingers from DB (will return a list of Finger objects)
    fingers = conn.get_templates()

    # to restore a finger, we need to assemble with the corresponding user
    # pass a User object and a list of finger (max 10) to save
    conn.save_user_template(user, [fing1 ,fing2])


def enroll_user():
    zk.enroll_user('1')
    # but it doesn't work with some tcp ZK8 devices

def attendance_record():
    # Get attendances (will return list of Attendance object)
    attendances = conn.get_attendance()
    # Clear attendances records
    conn.clear_attendance()


def test_voice():
    """
     play test voice:
      0 Thank You
      1 Incorrect Password
      2 Access Denied
      3 Invalid ID
      4 Please try again
      5 Dupicate ID
      6 The clock is flow
      7 The clock is full
      8 Duplicate finger
      9 Duplicated punch
      10 Beep kuko
      11 Beep siren
      12 -
      13 Beep bell
      14 -
      15 -
      16 -
      17 -
      18 Windows(R) opening sound
      19 -
      20 Fingerprint not emolt
      21 Password not emolt
      22 Badges not emolt
      23 Face not emolt
      24 Beep standard
      25 -
      26 -
      27 -
      28 -
      29 -
      30 Invalid user
      31 Invalid time period
      32 Invalid combination
      33 Illegal Access
      34 Disk space full
      35 Duplicate fingerprint
      36 Fingerprint not registered
      37 -
      38 -
      39 -
      40 -
      41 -
      42 -
      43 -
      43 -
      45 -
      46 -
      47 -
      48 -
      49 -
      50 -
      51 Focus eyes on the green box
      52 -
      53 -
      54 -
      55 -
    """
    conn.test_voice(index=0) # will say 'Thank You'


def device_maintainance():
    # DANGER!!! This command will be erase all data in the device (incuded: user, attendance report, and finger database)
    conn.clear_data()
    # shutdown connected device
    conn.poweroff()
    # restart connected device
    conn.restart()
    # clear buffer
    conn.free_data()


def live_attendance():
    # live capture! (timeout at 10s)
    for attendance in conn.live_capture():
        if attendance is None:
            # implement here timeout logic
            pass
        else:
            print (attendance) # Attendance object

        #if you need to break gracefully just set
        #   conn.end_live_capture = True
        #
        # On interactive mode,
        # use Ctrl+C to break gracefully
        # this way it restores timeout
        # and disables live capture

def enable_disable_device():
    # disable (lock) device, to ensure no user activity in device while some process run
    conn.disable_device()
    # re-enable the connected device and allow user activity in device again
    conn.enable_device()


def get_set_time():
    from datetime import datetime
    # get current machine's time
    zktime = conn.get_time()
    print(zktime)
    # update new time to machine
    newtime = datetime.today()
    conn.set_time(newtime)

def device_information():
    conn.get_firmware_version()
    conn.get_serialnumber()
    conn.get_platform()
    conn.get_device_name()
    conn.get_face_version()
    conn.get_fp_version()
    conn.get_extend_fmt()
    conn.get_user_extend_fmt()
    conn.get_face_fun_on()
    conn.get_compat_old_firmware()
    conn.get_network_params()
    conn.get_mac()
    conn.get_pin_width()


def device_usage_options():
    conn.read_sizes()
    print(conn)
    #also:
    conn.users
    conn.fingers
    conn.records
    conn.users_cap
    conn.fingers_cap
    # TODO: add records_cap counter
    # conn.records_cap


conn = None
zk = ZK('192.168.1.201', port=4370, timeout=5)
try:
    print('Connecting to device ...')
    conn = zk.connect()
    print('Disabling device ...')
    conn.disable_device()
    print('Firmware Version: : {}'.format(conn.get_firmware_version()))

    # print '--- Get User ---'
    # conn.delete_user(uid=11)
    print("Voice Test ...")
    conn.test_voice()
    print('Enabling device ...')
    conn.enable_device()  

except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()


