import json
import kirara_redraw

dropItems = "2012:900,2013:900,2014:900,2015:900,2016:100,2017:900"

kirara_api = kirara_redraw.redraw()

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
