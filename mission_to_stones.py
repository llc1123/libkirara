import libkirara
import time

kirara_api = libkirara.KiraraAPI()
kirara_api.set_user_agent("Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9060C Build/KOT49H)")
kirara_api.set_unity_user_agent("app/0.0.0; Android OS 4.4.2 / API-19 KOT49H/3.8.017.1018; samsung GT-I9060C")

kirara_api.load_account_and_login()

r = kirara_api.mission_get()
print(r)
r.pop("resultCode")
r.pop("resultMessage")
r.pop("serverTime")
r.pop("serverVersion")

originals = {}
for item in r["missionLogs"]:
    item.pop("playerId")
    item["reward"] = None
    originals[item["managedMissionId"]] = item["rate"]
    item["rate"] = item["rateMax"]

# Ctrl-Break(Windows)/Ctrl-C(Linux) to break the loop; Press only ONCE!!!
try:
    while True:
        t = kirara_api.mission_set(r)
        print(t)

        for item in r["missionLogs"]:
            if item["rateMax"] < 3:
                continue
            mission_dict = {
                "managedMissionId": item["managedMissionId"]
            }
            t = kirara_api.mission_complete(mission_dict)
            print(t)
            time.sleep(0.1)
except:
    pass

# DO NOT INTERRUPT THIS REQUEST!!!
for item in r["missionLogs"]:
    item["rate"] = originals[item["managedMissionId"]]
t = kirara_api.mission_set(r)
print(t)
