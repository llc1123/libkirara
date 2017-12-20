import time
import json
import uuid
import logging
import random
import libkirara

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s][%(funcName)-2s]-> %(message)s',
                    datefmt='%m-%d %H:%M:%S')

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
# move get switch
move_get_flag = False

# login with a.d
# kirara_api.load_account()
# kirara_api.login(kirara_api.user_account["uuid"],kirara_api.user_account["accesstoken"])

# login with uuid & accesstoken
# kirara_api.login("","")

# login with session id
# kirara_api.session_id = ""

# login with new account
name = "きらら"
uuid_a = str(uuid.uuid4())
accesstoken_a = kirara_api.signup(uuid_a,name)
kirara_api.login(uuid_a,accesstoken_a)
move_get_flag = True

kirara_api._make_request(
    "/api/player/gacha/draw", 
    {"gachaId":1,"drawType":3,"stepCode":0,"reDraw":True},True)

while True:
    r = kirara_api._make_request(
        "/api/player/gacha/draw", 
        {"gachaId":1,"drawType":3,"stepCode":4,"reDraw":False},True)
    try:
        result = check_count(r)
        print(result)
        if result["gold"] == 8:
            break
    except KeyError:
        print("session invalid")
    time.sleep(1+random.uniform(1, 2))

# new id move get
if move_get_flag:
    print("UUID: %s, TOKEN: %s" % (uuid_a,accesstoken_a))
    print("MoveCode: %s" % kirara_api.move_get("kirara"))