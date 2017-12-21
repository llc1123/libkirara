# -*- coding: UTF-8 -*-
import requests
import json
import time
from multiprocessing.dummy import Pool

status = [0]*30

def search(id):
    global status
    if id[0] == -1:
        return True
    if id[0] == 0:
        while True:
            print(status)
            time.sleep(1)

    headers = {
        'Unity-User-Agent': 'app/0.0.0; Android OS 5.1.1 / API-22 LMY48Z/eng..20171128.154408; samsung SM-G955F',
        'X-STAR-REQUESTHASH': id[1],
        'X-Unity-Version': '5.5.4f1',
        'X-STAR-AB': '3',
        'X-STAR-SESSION-ID': id[2],
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G955F Build/LMY48Z)',
        'Host': 'krr-prd.star-api.com',
    }

    data = '{"gachaId":1,"drawType":3,"stepCode":0,"reDraw":true}'

    ssr_list = {
        10002000:"Yuno",
        11002000:"Yuzuko",
        12002000:"Yuki",
        13002000:"Tooru",
        14002000:"Karen",
        15002000:"Aoba",
        16002000:"Tamaki",
        17002000:"Chiya"
    }

    count = 0
    while True:
        try:
            r = requests.post('https://krr-prd.star-api.com/api/player/gacha/draw', headers=headers, data=data)
            result = json.loads(r.content)
            ssr = []
            for i in range(len(result['managedCharacters'])):
                if(result['managedCharacters'][i]['levelLimit'] == 50):
                    cid = result['managedCharacters'][i]['characterId']
                    ssr.append(cid)
                    #print(ssr_list[cid])
                    count=count+1
            #print('SSR Count:'+str(count))
            if(count >= id[3]) :
                for j in range(len(ssr)):
                    ssr[j]=ssr_list[ssr[j]]
                requests.post('https://sc.ftqq.com/SCU17834Td7ffd306e471941f6cf329b0a03196af5a2ce6863c713.send?text=Kirara_Bot_'+str(id[0])+'&desp='
                    +'_'.join(ssr)
                    )
                return True
            count = 0
            status[id[0]-1] += 1
        except:
            print(u'Server Error')
            status[id[0]-1] += 1
        else:
            #print(u'---------Attempts: '+str(c))
            pass

id_list = [
            [0],
            [-1],
            [-1],
            [3,'3bed82fc3b6ef5332a401a29d9e979a793c43fe751e4d9deb06a4747df9234c3','3b35f461-423c-4cd9-85e1-92a5fe5a9f9d',4],
            [-1],
            [-1],
            [6,'06803108771623445f500633304d874b5f70dba6b0c87d87a1786ddaa21f8398','e33167eb-548a-4dc1-94b5-6743302b2b65',4],
            [-1],
            [8,'d3cc06686061c01b254f43e39e542bdfa0c746586bbfa8791ea3d4c26dc6aea5','93aedd54-6ce7-49e8-98f0-89471b11d89b',4],
            [9,'a4e9454c54d5dbf5ec98a90aa1dbbfc347ce5e831a1acf88987a8c5bb7363ffa','896477b0-95a9-46b1-b46c-6e06b1272356',4],
            [-1],
            [11,'bcbef677a95e1432b1a437f7d588259625b71666a9123abb3dab7946bbd5f96c','3c78f0c6-4adc-40b1-b7aa-291907adc745',4],
            [12,'a9e7ca315db1b917c5356f7028d68153724c2e7e2c5d47d82316f2a3c44959fa','74b08b76-c768-48a1-8acd-f691d0d1aeb0',4],
            [13,'9865698fefe5a92750b1a9235f687709b290793e562583caa486b8aaa4b20838','6e88a953-c9ac-4306-a7a8-1fb7d12e88c3',4],
            [-1],
            [15,'7a6036cf90d7848fd79d4d41c2910f90f5d81cfcc9f416c3d8e1382cc804dc55','5ac96db8-2811-4698-bdf2-86516915533c',4],
            [16,'8880efe8a43b541f7e06d3c1f55338c9c9654a43d33b65ffd0acea1d984fecbd','8e1fc1e1-568f-4179-b33a-c1c82cfb0243',4],
            [-1],
            [18,'58980ea733f0787bf1b1e110e91d936278b1037ec627d109ccfe2c1e7860172d','4afbe9c7-4fc2-40bc-a693-4d08e293afdc',4],
            [-1],
            [20,'fa932e58301b198e2e822b28c5cf0b8827c43af76fbe97098dc408158bc7718a','85e32725-54b7-484b-96d0-6f04b4a52bdc',4],
            [21,'2920bbe32ec6e1f33e9d23056a6b64d639997286126adc80f262ac3463eeafa7','a91f91a8-c49c-4a4f-9cfe-ccf0a2bd1117',5],
            [22,'fd55b49ddd53d8c30427bd0b68c8187eed6543f8f0d5e7e7180bb8ab9a460ad1','73203718-a425-46d4-8306-001514f82d1e',5],
            [23,'21e727f7af5b36c8be97d3cce3a75567bd04e3f808a9192dc14dfa17c09954eb','c6b24315-cba3-4fb9-a91a-c9dd04bd7088',5],
            [24,'365ff4d3cf6dbea8afe4abd4f67e7494ed8926d783b4cd3f82652bd9e97a5989','ff38231f-5f66-49e3-97bf-7bd30c280cd6',5],
            [25,'36a9b636bfdfcdaf0b02180d2eaf2d1e5905486f16bfb5eeaab8697feb69f271','44296e72-8d22-4601-9c4d-79c1cb7a27f9',5],
            [26,'a5313ebf68df0771e7e71fbe545fc91af8de436bdd79e2263bc0e033e64dc5f9','9839d256-79b9-4a3a-9919-89f3b667aaf2',5],
            [27,'7af61a7396c8041cea40e3edebaf98a589e85cd4e29da7c65b56dbc7732c9908','826ba565-1072-48bb-b827-4ef649c4aa1e',5],
            [28,'313465da09605279449bcebb3b18899ce6962c9a78698ab04a713d6d4e005404','b63365b6-ac5a-49bd-bf7c-26851bc9ca4d',5],
            [29,'cabf4674cdf9a9f38c9c18f9917eb0de753d8a0c3d3aef002d4e8e1b4c6bcbdc','664dcdbe-dc0f-4a47-8df1-25fbf5e9f5fb',5],
            [30,'9668c93863ab403c81f404db07c082e31a25ab68553af0e63e907c45dc080ed8','936ac5cf-cd31-4011-9574-ff46e016d08d',5]
        ]
pool = Pool(31)
results = pool.map(search, id_list)