import urllib.request as ur
request = ur.Request(
    url='https://edu.csdn.net/mycollege',
    headers={
        'User-Agent':'',
        'Cookie':'uuid_tt_dd=10_37409216830-1608607271556-285638; dc_session_id=10_1608607271556.588292; dc_sid=4444a1371e6993ef2185a100e79ec760; SESSION=e46c74d9-e9ad-4ba1-b043-2b86583bea50; c_first_ref=default; c_first_page=https%3A//passport.csdn.net/login%3Fcode%3Dpublic; c_segment=6; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1608607372; is_advert=1; announcement-new=%7B%22isLogin%22%3Afalse%2C%22announcementUrl%22%3A%22https%3A%2F%2Flive.csdn.net%2Froom%2Fpy_ai_326%2F9MUeZ9A7%3Futm_source%3Dgonggao_1201%22%2C%22announcementCount%22%3A0%2C%22announcementExpire%22%3A3600000%7D; UserName=blackblacksky; UserInfo=c5f3d8698fd540bda0a5c40c2ef85180; UserToken=c5f3d8698fd540bda0a5c40c2ef85180; UserNick=%E9%94%A4%E7%9A%84%E7%A8%80%E7%83%82%E7%9A%84%E9%93%9C%E8%B1%86%E8%B1%86; AU=D68; UN=blackblacksky; BT=1608607422466; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22blackblacksky%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_37409216830-1608607271556-285638!5744*1*blackblacksky; log_Id_view=10; c_pref=https%3A//edu.csdn.net/content/training; c_ref=https%3A//edu.csdn.net/content/live; log_Id_click=6; c_page_id=default; dc_tos=qlq2gh; log_Id_pv=13; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1608608754'
    }
)

response = ur.urlopen(request).read().decode('utf-8')