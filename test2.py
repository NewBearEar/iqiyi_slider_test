import execjs
import re
import json
import random
import time
import requests
from img_locate import get_distance
from process_trace import get_risk_data
import iqiyi_crypt

def init_slider(token, sid):
    """
    初始化滑块
    :param token:
    :param aes_key: AES 密钥
    :param hmac_key hmac 密钥
    :param sid: 密钥认证参数
    :return:
    """
    url = 'https://qcaptcha.iqiyi.com/api/outer/verifycenter/initpage'

    #origin_data = self.format_origin_data(token)
    cryptsrc_data = '38f5cbf50ecac64bf9e2571b89b693ddfaa094a3608f4df0d04ea0e58eff03a9dad2ad3228db30bd9cd69ecd4fa4c68f354ad1664bb11619c44a54cbf480e7193b50503273fa15890180748b9884017ca35c28f1151f8f6682bd8fcc96e6f136fdc5dbe7f8cb31bdfefd9ddae0ae82db6e4cc2df202ba11a676de3bdd42a19c94d6f0d4196b69f07fe56c098adb8d49328466541faefc4e321331713b265bb0961c95dfaaa8fb22c37f129533c21b36be7bf27043ed2d2f2a82016e16e13f002df991087520df96554253df415a8527ee4e1245a94dcba37e9d025bf3a3b756b19c53eb102024e10c8a98e34bfe8b8e8566a5bd779a6c025e1be1163a723e9bccce2fb92aac14fcdb03d846ddc35f05ca3073d6ebf3620357235e153b982f5cb|225234FA0EADF538D07EEF144F6ACE19F2492F136B6D84A15699DB354C7EF1A7'
    encrypt_data = {
        'cryptSrcData': cryptsrc_data,
        'cryptVersion': 'web|20180418xkdewxe3dkxu9|' + sid,
        'platform': 'web',
        'nifc': 'false'
    }
    session = requests.session()
    session.headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.iqiyi.com',
        'Referer': 'https://www.iqiyi.com/iframe/loginreg?ver=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    }

    # print('提交表单: {}'.format(encrypt_data))
    resp = session.post(url, data=encrypt_data)
    # print('验证码初始化接口返回加密数据: {}'.format(resp.text))
    #decrypt_data = json.loads(iqiyi_crypt.aes_decrypt(aes_key, resp.text.split('|')[0])[:-4])
    # print('AES 解密后数据: {}'.format(decrypt_data))
    #init_data = decrypt_data['data']['initData']

    print(resp.text.split('|')[0])
    #return init_data


with open('encrypt_pwd.js', encoding='utf-8') as f:
    aiqiyi = f.read()
js = execjs.compile(aiqiyi)
logid = js.call('rsaFun', "alyj0824")
#logid = js.call('get_pwd', "12345")
#print(logid)

print(logid)
sid = '78FC6CDE2BFA106F2E5CE09472AB8A43AD6E2E381A099C36875DBA96EA072A27D05DF2E79ABB6AE7B3A2FA93853B001C587876EA91677758EEA00B46010CEF405A78B1C59ACA33875FB18B0886E3BBBA6CB0646004128E3418536FDBB397B3A1287492CBD1F2DCD727B426FF797391A048C4E1C3BEF766C50ACC15A732EB0F43684D4BE59E9A929EFA02D8175EAB35119A8D515B95265CCDC144BF3737A779A26072EDB230CFED3CA7D579070A5EBDA383CABBE0AE4ACC840EA2F47A7CDDE3D754D39B61859828C2EB4C72AE9B717150E7ECB3E2CDB7E29B38A9978495D556CCEE7E7C10D613D9563B5E7D4BD05202AD519D9AA5A87B401DFC11441E343D20379B15667BB3A81431AB1F09449E90513AB50168312C2A9AD2F3A4054E9E15ED5B8FD72C6551065FB007E49C00D7763B4E218649151A5C683B1D3152FFB8EE7E2578A4EF9BEBF96433E33DC00A72F13CD9'
token = 'ed55464298d54075a68ec81edc749bd0'

init_slider(token,sid)
