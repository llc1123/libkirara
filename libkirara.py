# -*- coding: UTF-8 -*-
import requests
import uuid
import json
import time
import hashlib
import urllib.parse
from Crypto.Cipher import AES
import struct
import warnings
warnings.filterwarnings("ignore")

# proxies = {
#   'http': 'socks5://127.0.0.1:1800',
#   'https': 'socks5://127.0.0.1:1800'
# }

# proxies = {
#   'http': 'http://127.0.0.1:8888',
#   'https': 'http://127.0.0.1:8888'
# }

proxies = {}

class KiraraAPI:

    uuid = ''
    sessionId = ''
    accessToken = ''

    def loadAccount(self, path="a.d"):

        print("Loading account file...", end = '')
        
        encryptKey = b'7gyPmqc54dVNB3Te6pIpd2THj2y3hjOP'
        
        def unpad(data):
            return data[:-data[-1]]

        def parse_data(data):
            self.uuid = data[27:63].decode("UTF-8")
            self.accessToken = data[80:116].decode("UTF-8")

        with open(path, 'rb') as f:
            a = f.read(1)[0] & 0x7f
            f.read(3)
            pwlen = f.read(1)[0] - a
            pw = bytearray(f.read(pwlen))
            for i in range(0, pwlen):
                pw[i] -= 96 + i
            count, = struct.unpack('<i', f.read(4))
            cdata = f.read(count)
            aes = AES.new(encryptKey, AES.MODE_CBC, bytes(pw))
            data = unpad(aes.decrypt(cdata))
            parse_data(data)

        print("Complete")

    def manual(self, a, b):
        self.uuid = a
        self.accessToken = b

    def getHash(self, url, payload):
        salt = '85af4a94ce7a280f69844743212a8b867206ab28946e1e30e6c1a10196609a11'
        text = ((self.sessionId + ' ') if self.sessionId else '') \
                + url + ' ' \
                + ((payload + ' ') if payload else '') \
                + salt
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def sendPost(self, url, payload):
        payload_encoded = json.dumps(payload, separators = (',',':'))
        host = 'https://krr-prd.star-api.com'
        headers = {
            'Unity-User-Agent': 'app/0.0.0; Android OS 5.1.1 / API-22 LMY48Z/eng..20171128.154408; samsung SM-G955F',
            'X-STAR-REQUESTHASH': self.getHash(url, payload_encoded),
            'X-Unity-Version': '5.5.4f1',
            'X-STAR-AB': '3',
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G955F Build/LMY48Z)',
            'Host': 'krr-prd.star-api.com',
        }
        if self.sessionId:
            headers['X-STAR-SESSION-ID']=self.sessionId

        return requests.post(host + url, headers = headers, data = payload_encoded, proxies = proxies, verify=False)

    def sendGet(self, url, params):
        host = 'https://krr-prd.star-api.com'
        headers = {
            'Unity-User-Agent': 'app/0.0.0; Android OS 5.1.1 / API-22 LMY48Z/eng..20171128.154408; samsung SM-G955F',
            'X-STAR-REQUESTHASH': self.getHash(url+(('?'+urllib.parse.urlencode(params)) if params else ''), ''),
            'X-Unity-Version': '5.5.4f1',
            'X-STAR-AB': '3',
            'Content-Type': 'application/json; charset=UTF-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G955F Build/LMY48Z)',
            'Host': 'krr-prd.star-api.com',
        }
        if self.sessionId:
            headers['X-STAR-SESSION-ID']=self.sessionId

        return requests.get(host + url, headers = headers, params = params, proxies = proxies, verify=False)

    def getVersion(self):
        print('Checking version...', end = '')
        result = self.sendGet('/api/app/version/get', {'platform': '2', 'version': '1.0.3'})
        if result.ok:
            if json.loads(result.content)['resultCode'] == 0:
                print('OK.')
                return True 
            else:
                print('Failed: Server is down (again). Result Code: ' + str(json.loads(result.content)['resultCode']))
                return False
        else:
            print('Failed: Server is down (again).')
            return False

    def signUp(self):
        print('Signing up...', end = '')
        self.uuid = str(uuid.uuid4())
        result = self.sendPost('/api/player/signup', {"uuid":self.uuid,"platform":2,"name":"llc","stepCode":1})
        if result.ok:
            if json.loads(result.content)['resultCode'] == 0:
                self.accessToken = json.loads(result.content)['accessToken']
                print('Complete.')                                
                print('UUID: ' + self.uuid)
                print('AccessToken: ' + self.accessToken)
                return True
            else:
                print('Failed: Server is down (again). Result Code: ' + str(json.loads(result.content)['resultCode']))
                return False
        else:
            print('Failed: Server is down (again).')
            return False

    def login(self):
        print('Logging in...', end = '')
        result = self.sendPost('/api/player/login', {"uuid":self.uuid,"accessToken":self.accessToken,"platform":2,"appVersion":"1.0.3"})
        if result.ok:
            if json.loads(result.content)['resultCode'] == 0:
                self.sessionId = json.loads(result.content)['sessionId']
                print("Complete.")
                print("Session ID: " + self.sessionId)
                return True
            else:
                print('Failed: Server is down (again). Result Code: ' + str(json.loads(result.content)['resultCode']))
                return False
        else:
            print('Failed: Server is down (again).')
            return False

    def miscFirstLogin(self):
        print('Initializing for the first login...', end = '')
        self.sendGet('/api/player/get_all', '')
        self.sendGet('/api/player/quest/get_all', '')
        self.sendGet('/api/quest_chapter/get_all', '')
        self.sendGet('/api/player/mission/get_all', '')
        result = self.sendGet('/api/player/present/get_all', '')
        present = []
        for item in json.loads(result.content)['presents']:
            present.append(item['managedPresentId'])
        self.sendGet('/api/player/present/get', {'managedPresentId':','.join(str(x) for x in present), 'stepCode': 2})
        self.sendPost('/api/player/adv/add', {'advId':'1000000','stepCode':3})
        self.sendGet('/api/player/gacha/get_all', {'gachaIds':1})
        print('Complete.')

    def gachaLoop(self):
        cards = 0
        attemps = 0
        while cards < 116:
            result = json.loads(self.sendPost('/api/player/gacha/draw', {"gachaId":1,"drawType":3,"stepCode":4,"reDraw":False}).content)
            cards = len(result['managedCharacters'])
            attemps += 1
            print('Drawing Init Gacha...Attempts: ' + str(attemps) + ', Current Cards: ' + str(cards), end = '\r')
        print()

    def gachaChrist(self):
        self.sendGet('/api/player/gacha/get_all', {'gachaIds':''})
        cards = 0
        attemps = 0
        while cards < 120:
            result = json.loads(self.sendPost('/api/player/gacha/draw', {"gachaId":3,"drawType":3,"stepCode":0,"reDraw":False}).content)
            cards = len(result['managedCharacters'])
            attemps += 1
            print('Drawing Christmas Limited Gacha...Attempts: ' + str(attemps) + ', Current Cards: ' + str(cards), end = '\r')
        print()

    def fetchPresents(self):
        print('Fetching presents...', end = '')
        result = json.loads(self.sendGet('/api/player/present/get_all', '').content)
        present = []
        for item in result['presents']:
            present.append(item['managedPresentId'])
        while len(present)>99:
            self.sendGet('/api/player/present/get', {'managedPresentId':','.join(str(x) for x in present[0:99]), 'stepCode': 0})
            present = present[99:]
        self.sendGet('/api/player/present/get', {'managedPresentId':','.join(str(x) for x in present), 'stepCode': 0})
        print('Complete.')
        
    def move(self):
        print('Generating moving code...', end = '')
        result = self.sendPost('/api/player/move/get', {'password':'1234'})
        print('Complete.')
        print('Moving Code: ' + json.loads(result.content)['moveCode'])
        print('Password: 1234')


    daily = range(1,6)
    weekly = range(1000,1006)
    f5 = 40015

    dailySet = {'missionLogs':[]}
    weeklySet = {'missionLogs':[]}
    f5Set = {'missionLogs':[]}
    otherSet = {'missionLogs':[]}

    def mission_refresh(self):
        print('Refreshing mission list...', end = '')
        result = json.loads(self.sendGet('/api/player/mission/get_all','').content)['missionLogs']
        self.dailySet = {'missionLogs':[]}
        self.weeklySet = {'missionLogs':[]}
        self.f5Set = {'missionLogs':[]}
        self.otherSet = {'missionLogs':[]}
        for i in result:
            item = {"managedMissionId":i['managedMissionId'], "missionId":i['missionId'], "subCode":i['subCode'], "rate":i['rate'], "rateMax":i['rateMax'], "state":i['state'], "reward":None, "limitTime":i['limitTime']}
            if item['missionId'] in self.daily:
                self.dailySet['missionLogs'].append(item)
            elif item['missionId'] in self.weekly:
                self.weeklySet['missionLogs'].append(item)
            elif item['missionId'] == self.f5:
                self.f5Set['missionLogs'].append(item)
            else:
                self.otherSet['missionLogs'].append(item)
        print('Complete.')

    def mission_complete(self, missionList):
        self.sendPost('/api/player/mission/set', missionList)

        for i in missionList['missionLogs']:
            self.sendPost('/api/player/mission/complete', {'managedMissionId':i['managedMissionId']})

    def mission_reset(self, missionList):
        self.sendPost('/api/player/mission/set', missionList)

    def mission_completeDaily(self):
        print('Completing daily missions...', end = '')
        self.mission_complete(self.dailySet)
        print('Complete.')

    def mission_completeWeekly(self):
        print('Completing weekly missions...', end = '')
        self.mission_complete(self.weeklySet)
        print('Complete.')

    def mission_completeF5(self):
        print('Completing friendliness-5 missions...', end = '')
        self.mission_complete(self.f5Set)
        self.mission_reset(self.f5Set)
        print('Complete.')

    def mission_completeOther(self):
        print('Completing Other missions...', end = '')
        self.mission_complete(self.otherSet)
        print('Complete.')


    def dropAll(self):
        r = self.sendPost('/api/player/quest_log/add', {'managedBattlePartyId': -1, 'questId': 1100010, 'supportCharacterId': -1, 'type': 3})
        orderReceiveId = json.loads(r.content)['orderReceiveId']
        dropItems = '1:999,2:999,3:999,4:999,5:999,6:999,7:999,8:999,9:999,10:999,' + \
                    '11:999,12:999,13:999,14:999,15:999,16:999,17:999,18:999,19:999,20:999,21:999,' + \
                    '1000:999,1001:999,1002:999,1003:999,1004:999,' + \
                    '2000:999,2001:999,2002:999,2003:999,2004:999,2005:999,2006:999,2007:999,2008:999,2009:999,2010:999,' + \
                    '2011:999,2012:999,2013:999,2014:999,2015:999,2016:999,2017:999,2018:999,2019:999,2020:999,2021:999,' + \
                    '2022:999,2023:999,' + \
                    '3000:999,3001:999,3002:999,3003:999,3004:999,3005:999,3006:999,3007:999,' + \
                    '4000:999,4001:999,4002:999,4003:999,4004:999,4005:999,4006:999,4007:999,4008:999,4009:999,4010:999,' + \
                    '4011:999,4012:999,4013:999,4014:999,' + \
                    '5000:999,5001:999,5002:999,5003:999,5004:999,5005:999,5006:999,5007:999,' + \
                    '6000:999,6001:999,6002:999,6003:999,6004:999,6005:999,6006:999,6007:999,6008:999,6009:999,6010:999,' + \
                    '6011:999,6012:999,6013:999,6014:999,6015:999,6016:999,6017:999,6018:999,6019:999,6020:999,6021:999,' + \
                    '6022:999,6023:999,6024:999,6025:999,6026:999,6027:999,6028:999,6029:999,' + \
                    '7000:999,7001:999,7002:999,7003:999,7004:999,7005:999,7006:999,7007:999,7008:999,7009:999,7010:999,' + \
                    '7011:999,7012:999,7013:999,7014:999,' + \
                    '8000:999,8001:999,8002:999,8003:999,8004:999,8005:999,8006:999,8007:999,' + \
                    '9000:999,' + \
                    '10000:999,10001:999,' + \
                    '100100:999,100101:999,100102:999,100103:999,100104:999'

        self.sendPost('/api/player/quest_log/set', {
            'clearRank': 3,
            'dropItems': dropItems,
            'friendUseNum': 0,
            'killedEnemies': '',
            'masterSkillUseNum': 0,
            'orderReceiveId': orderReceiveId,
            'skillExps': '',
            'state': 2,
            'stepCode': 0,
            'uniqueSkillUseNum': 0,
            'weaponSkillExps': '' 
            })

        print('Add all items to 999...Complete.')
