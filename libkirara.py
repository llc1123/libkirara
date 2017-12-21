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
                print('Failed: Server is down (again). Result Code: ' + json.loads(result.content)['resultCode'])
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
                print('Failed: Server is down (again). Result Code: ' + json.loads(result.content)['resultCode'])
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
                print('Failed: Server is down (again). Result Code: ' + json.loads(result.content)['resultCode'])
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
        for i in missionList['missionLogs']:
            i['rate'] = i['rateMax']

        self.sendPost('/api/player/mission/set', missionList)

        for i in missionList['missionLogs']:
            self.sendPost('/api/player/mission/complete', {'managedMissionId':i['managedMissionId']})

    def mission_reset(self, missionList):
        for i in missionList['missionLogs']:
            i['rate'] = 0
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