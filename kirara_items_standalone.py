import json
import libkirara

item_list_range = True
item_range = [[2012,2017],]
item_count = 900
drop_items = "2012:900,2013:900,2014:900,2015:900,2016:100,2017:900"

def items_flusher(dropItems, kirara_api):
    r = kirara_api._make_request('/api/player/quest_log/add', {
        "managedBattlePartyId": -1,
        "questData": 'null',
        "questId": 1100010,
        "supportCharacterId": -1,
        "type": 3
    }, True)
    orderReceiveId = json.loads(r.decode("UTF-8"))['orderReceiveId']
    kirara_api._make_request('/api/player/quest_log/set', {
        "clearRank": 3,
        "dropItems": dropItems,
        "friendUseNum": 0,
        "killedEnemies": "",
        "masterSkillUseNum": 0,
        "orderReceiveId": orderReceiveId,
        "skillExps": "",
        "state": 2,
        "stepCode": 0,
        "uniqueSkillUseNum": 0,
        "weaponSkillExps": ""
    }, True)

def main():
    global drop_items
    # id range list of items
    if item_list_range:
        item_list = []
        for i in item_range:
            for j in range(i[0],i[1]+1):
                item_list.append("%d:%d" % (j,item_count))
        drop_items = ",".join(item_list)
    # login with a.d
    kirara_api = libkirara.KiraraAPI()
    kirara_api.load_account_and_login()
    items_flusher(drop_items, kirara_api)

if __name__ == "__main__":
    main()
