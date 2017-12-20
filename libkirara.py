# BASIC LIB
import requests
import json
import hashlib
import logging
import urllib.parse
# UNPACK A.D
try:
    from Crypto.Cipher import AES
except BaseException:
    print('WARNING: pycrypto not found, cannot read a.d file')
import struct
# UNPACK Quests data
import base64
import zlib

PLATFORM = 2 # android
VERSION = '1.0.3'

logger = logging.getLogger('kirara')

### WARNING: SET YOUR OWN RANDOM USER-AGENT!! UPDATE THE HEADERS IF APP CHANGE!!
class KiraraAPI:
    
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.0.1; MI 3 Build/BGX29T)',
        'Unity-User-Agent': 'app/0.0.0; Android 5.0.1 / API-21 BGX29T/5445cf4e65; Xiaomi MI 3',
        'X-Unity-Version': '5.5.4f1',
        #'X-STAR-AB': '3',
    }
    user_account = {
        "ver": "","pwlen": "","pw": "","count": "",
        "uuid": "","accesstoken": "","mycode": ""
    }
    session_id = None
    
    def __init__(self):
        self.session = requests.Session()
    
    def load_account(self, path="a.d"):
        
        encryptKey = b'7gyPmqc54dVNB3Te6pIpd2THj2y3hjOP'
        
        def unpad(data):
            return data[:-data[-1]]

        def parse_data(data):
            self.user_account["uuid"] = data[27:63].decode("UTF-8")
            self.user_account["accesstoken"] = data[80:116].decode("UTF-8")
            self.user_account["mycode"] = data[126:].decode("UTF-8")

        with open(path, 'rb') as f:
            a = f.read(1)[0] & 0x7f
            self.user_account["ver"] = hex(f.read(1)[0])
            f.read(2)
            pwlen = f.read(1)[0] - a
            pw = bytearray(f.read(pwlen))
            for i in range(0, pwlen):
                pw[i] -= 96 + i
            self.user_account["pwlen"] = pwlen
            self.user_account["pw"] = pw
            count, = struct.unpack('<i', f.read(4))
            self.user_account["count"] = count
            cdata = f.read(count)
            aes = AES.new(encryptKey, AES.MODE_CBC, bytes(pw))
            data = unpad(aes.decrypt(cdata))
            parse_data(data)
        return self.user_account
    
    def load_account_and_login(self, path="a.d"):
        self.load_account(path)
        self.login(self.user_account["uuid"], self.user_account["accesstoken"])

    def set_user_agent(self, user_agent):
        self.headers['User-Agent'] = user_agent
    
    def set_unity_user_agent(self, unity_user_agent):
        self.headers['Unity-User-Agent'] = unity_user_agent
    
    def _make_request(self, api, data, post):
        if 'X-STAR-AB' not in self.headers:
            resultStr = self._make_request2('/api/app/version/get', {'platform': PLATFORM, 'version': VERSION}, post=False)
            logger.info(str(resultStr))
            result = json.loads(resultStr)
            self._assert_result(result)
            self.headers['X-STAR-AB'] = str(result['abVer'])
        return self._make_request2(api, data, post)
    
    def _make_request2(self, api, data, post):
        REQUESTHASH_SECRET = "85af4a94ce7a280f69844743212a8b867206ab28946e1e30e6c1a10196609a11"
        headers = dict(self.headers)
        if self.session_id is not None:
            headers['X-STAR-SESSION-ID'] = self.session_id
        elif 'X-STAR-SESSION-ID' in headers:
            del headers['X-STAR-SESSION-ID']

        datastr = ''
        for k in data:
            v = data[k]
            datastr += f'\"{k}\":{json.dumps(v)},'
        datastr = f'{{{datastr[:-1]}}}'

        if post:
            headers['Content-Length'] = str(len(datastr.encode()))
            headers['Content-Type'] = 'application/json; charset=UTF-8'

        if not post:
            api += '?' + urllib.parse.urlencode(data)
        bstring = api
        if 'X-STAR-SESSION-ID' in headers:
            bstring = headers['X-STAR-SESSION-ID'] + ' ' + bstring
        if post:
            bstring += ' ' + datastr
        bstring += f' {REQUESTHASH_SECRET}'
        sha = hashlib.sha256()
        sha.update(bstring.encode('utf8'))
        requestHash = sha.hexdigest()
        headers['X-STAR-REQUESTHASH'] = requestHash

        url = 'https://krr-prd.star-api.com' + api
        r = None
        if post:
            r = self.session.post(url, headers=headers, data=datastr.encode())
        else:
            r = self.session.get(url, headers=headers)
        return r.content
    
    def _assert_result(self, result, accepting=[0]):
        if result['resultCode'] not in accepting:
            raise KiraraException('ResultCode: ' + str(result['resultCode']))

    def signup(self, uuid, name):
        resultStr = self._make_request("/api/player/signup", {
            "uuid": uuid,
            "platform": PLATFORM,
            "name": name,
            "stepCode":1
        },True)
        result = json.loads(resultStr)
        self._assert_result(result)
        return result['accessToken']
    
    def login(self, uuid, access_token):
        self.session_id = None
        resultStr = self._make_request('/api/player/login', {
            'accessToken': access_token,
            'appVersion': VERSION,
            'platform': PLATFORM,
            'uuid': uuid
        }, True)
        logger.info(str(resultStr))
        result = json.loads(resultStr)
        self._assert_result(result)
        self.session_id = result['sessionId']
    
    def move_get(self, password):
        resultStr = self._make_request('/api/player/move/get', {
            'password': password
        }, True)
        logger.info(str(resultStr))
        result = json.loads(resultStr)
        self._assert_result(result)
        return result['moveCode']
    
    def move_set(self, move_code, password, uuid):
        resultStr = self._make_request('/api/player/move/set', {
            'moveCode': move_code,
            'movePassword': password,
            'uuid': uuid,
            'platform': PLATFORM
        }, True)
        logger.info(str(resultStr))
        result = json.loads(resultStr)
        self._assert_result(result)
        return result['accessToken']
    
    def age_set(self, age):
        resultStr = self._make_request('/api/player/age/set', {
            'age': age,
        }, True)
        logger.info(str(resultStr))
        result = json.loads(resultStr)
        self._assert_result(result)
        return True
    
    def mission_get(self):
        resultStr = self._make_request('/api/player/mission/get_all', {}, False)
        logger.info(str(resultStr))
        result = json.loads(resultStr)
        self._assert_result(result)
        return result
    
    def mission_set(self, mission_dict):
        resultStr = self._make_request('/api/player/mission/set', mission_dict, True)
        logger.info(str(resultStr))
        result = json.loads(resultStr)
        self._assert_result(result)
        return result
    
    def mission_complete(self, mission_dict):
        resultStr = self._make_request('/api/player/mission/complete', mission_dict, True)
        logger.info(str(resultStr))
        result = json.loads(resultStr)
        self._assert_result(result, [0, 510])
        return result

    def quests_data_unpack(self, q_data):
        step_0 = base64.b64decode(q_data)
        return json.loads("{%s}" % zlib.decompress(step_0).decode("UTF-8"))

    def quests_data_pack(self, q_data):
        q = zlib.compress(json.dumps(q_data)[1:-1].encode("UTF-8"))
        return base64.b64encode(q).decode("UTF-8")

class KiraraException(Exception):
    pass
