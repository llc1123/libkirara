import time
import json
import libkirara

def check_count(r: dict):
    cid_map = {
        "10002000":"ゆの",
        "11002000":"ゆずこ",
        "12002000":"ゆき",
        "13002000":"トオル",
        "14002000":"九条 カレン",
        "15002000":"涼風 青葉",
        "16002000":"本田 珠輝",
        "17002000":"千矢"
    }
    result_json = {
        "copper": 0,
        "silver": 0,
        "gold": 0
    }
    game_json = json.loads(r.decode("UTF-8"))
    CID = []
    for item in game_json["managedCharacters"]:
        type = item["levelLimit"]
        if type == 50:
            result_json["gold"] += 1
            CID.append(item["characterId"])
            logging.info("CID: %d" % item["characterId"])
        if type == 40:
            result_json["silver"] += 1
        if type == 30:
            result_json["copper"] += 1
    if CID:
        crs = ""
        crs += ", ".join([cid_map[str(i)] for i in CID])
        print(crs)
    return result_json


kirara_api = libkirara.KiraraAPI()
kirara_api.set_user_agent("Dalvik/1.6.0 (Linux; U; Android 4.4.2; GT-I9060C Build/KOT49H)")
kirara_api.set_unity_user_agent("app/0.0.0; Android OS 4.4.2 / API-19 KOT49H/3.8.017.1018; samsung GT-I9060C")
# load account from a.d
# kirara_api.load_account()
# kirara_api.login(kirara_api.user_account["uuid"],kirara_api.user_account["accesstoken"])
# using session id
kirara_api.session_id = ""

kirara_api._make_request(
    "/api/player/gacha/draw", 
    {"gachaId":1,"drawType":3,"stepCode":0,"reDraw":True},True)

while True:
    r = kirara_api._make_request(
        "/api/player/gacha/draw", 
        {"gachaId":1,"drawType":3,"stepCode":4,"reDraw":False},True)
    try:
        print(check_count(r))
    except KeyError:
        print("session invalid")
    
