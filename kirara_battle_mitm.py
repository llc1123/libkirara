"""修改 kirara 战斗数据（配合 mitmproxy 使用）
以下代码以修改物品掉落为例
亦可以稍作修改用户修改每一回合的战斗结果详情（人物/技能状态之类的）
API 说明：
    quest_log/add
        开始战斗，必要。体力消耗取决于选择的地图。
    quest_log/save
        战斗中战局保存，每一局开始前至少发送一次。
        但是是否发送成功不影响客户端游戏。
    quest_log/set
        战斗结束结算。掉落数据和人物技能经验都在这提交。
"""

from mitmproxy import http
import json
import base64
import zlib
import hashlib

item_range = [
    [2012,2017],
]
item_count = 900
item_list = []
for i in item_range:
    for j in range(i[0],i[1]+1):
        item_list.append("%d:%d" % (j,item_count))
item_list = ",".join(item_list)

def quests_data_unpack(q_data):
    step_0 = base64.b64decode(q_data)
    return json.loads("{%s}" % zlib.decompress(step_0).decode("UTF-8"))

def quests_data_pack(q_data):
    q = zlib.compress(json.dumps(q_data)[1:-1].encode("UTF-8"))
    return base64.b64encode(q).decode("UTF-8")

def calc_requests_hash(game_session, api_string, json_string):
    reqhash_secret = "85af4a94ce7a280f69844743212a8b867206ab28946e1e30e6c1a10196609a11"
    base_string = "%s %s %s %s" % (game_session,api_string,json_string,reqhash_secret)
    byte_hash = hashlib.sha256(base_string.encode("UTF-8"))
    return byte_hash.hexdigest()

def battle_mitm(save_json):
    save_json["dropItems"] = item_list
    return save_json

def request(flow: http.HTTPFlow) -> None:
    
    def inject(url_path):
        af_json = battle_mitm(json.loads(flow.request.content))
        flow.request.content = json.dumps(af_json).encode("UTF-8")
        flow.request.headers["X-STAR-REQUESTHASH"] = calc_requests_hash(
            flow.request.headers["X-STAR-SESSION-ID"],
            url_path,
            json.dumps(af_json)
        )
        flow.request.headers["Content-Length"] = str(len(flow.request.content))
    
    api_path = [
        "/api/player/quest_log/set",
    ]
    if flow.request.pretty_host == "krr-prd.star-api.com":
        for url_path in api_path:
            if flow.request.path.startswith(url_path):
                inject(url_path)
