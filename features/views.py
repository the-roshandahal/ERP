from django.shortcuts import render
from zk import ZK, const
# Create your views here.
def home(request):
    conn = None
    zk = ZK('192.168.1.254', port=4370, timeout=10,password=123, force_udp=False, ommit_ping=False)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        # another commands will be here!
        # Example: Get All Users
        users = conn.get_users()
        for user in users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            print ('+ UID #{}'.format(user.uid))
            print ('  Name       : {}'.format(user.name))
            print ('  Privilege  : {}'.format(privilege))
            print ('  Password   : {}'.format(user.password))
            print ('  Group ID   : {}'.format(user.group_id))
            print ('  User  ID   : {}'.format(user.user_id))

        # Test Voice: Say Thank You
        conn.test_voice()
        # re-enable device after all commands already executed
        conn.enable_device()
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()
    # try:
    #     print ('Connecting to device ...')
    #     conn = zk.connect()
    #     print ('Disabling device ...')
    #     conn.disable_device()
    #     print ('Firmware Version: : {}'+format(conn.get_firmware_version()))
    #     # print '--- Get User ---'
    #     users = conn.get_users()
    #     for user in users:
    #         privilege = 'User'
    #         if user.privilege == const.USER_ADMIN:
    #             privilege = 'Admin'

    #         print ('- UID #{}'+ format(user.uid))
    #         print ('  Name       : {}'+format(user.name))
    #         print ('  Privilege  : {}'+format(privilege))
    #         print ('  Password   : {}'+format(user.password))
    #         print ('  Group ID   : {}'+format(user.group_id))
    #         print ('  User  ID   : {}'+format(user.user_id))

    #     print ("Voice Test ...")
    #     conn.test_voice()
    #     print ('Enabling device ...')
    #     conn.enable_device()
    # except (Exception):
    #     print ("Process terminate" )
    # finally:
    #     if conn:
    #         conn.disconnect()
    return render (request,'index.html')