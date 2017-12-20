import libkirara
import time

kirara_api = libkirara.KiraraAPI()
kirara_api.set_user_agent("Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9060C Build/KOT49H)")
kirara_api.set_unity_user_agent("app/0.0.0; Android OS 4.4.2 / API-19 KOT49H/3.8.017.1018; samsung GT-I9060C")

kirara_api.load_account()
kirara_api.login(kirara_api.user_account["uuid"],kirara_api.user_account["accesstoken"])

while True:
    r = kirara_api.mission_get()
    r.pop("resultCode")
    r.pop("resultMessage")
    r.pop("serverTime")
    r.pop("serverVersion")
    for item in r["missionLogs"]:
        item.pop("playerId")
        item["reward"] = None
        item["rate"] = item["rateMax"]
    t = kirara_api.mission_set(r)
    print(t)
    for item in r["missionLogs"]:
        mission_dict = {
            "managedMissionId": item["managedMissionId"]
        }
        try:
            t = kirara_api.mission_complete(mission_dict)
            print(t)
        except:
            pass
        time.sleep(0.1)