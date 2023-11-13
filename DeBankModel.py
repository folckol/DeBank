
import json
import random
import re
import ssl
import imaplib
import email
import string
import time
import traceback
import urllib
import uuid
from datetime import datetime

import ua_generator
from requests.cookies import RequestsCookieJar
from web3 import Web3

import capmonster_python
import requests
import cloudscraper
from eth_account.messages import encode_defunct
from web3.auto import w3

def random_user_agent():
    browser_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{0}.{1}.{2} Edge/{3}.{4}.{5}'
    ]

    chrome_version = random.randint(70, 108)
    firefox_version = random.randint(70, 108)
    safari_version = random.randint(605, 610)
    edge_version = random.randint(15, 99)

    chrome_build = random.randint(1000, 9999)
    firefox_build = random.randint(1, 100)
    safari_build = random.randint(1, 50)
    edge_build = random.randint(1000, 9999)

    browser_choice = random.choice(browser_list)
    user_agent = browser_choice.format(chrome_version, firefox_version, safari_version, edge_version, chrome_build, firefox_build, safari_build, edge_build)

    return user_agent

def get_last_mail(login, password):
    count = 0
    while count < 5:

        count+=1

        # Введите свои данные учетной записи
        email_user = login
        email_pass = password

        if '@rambler' in login or '@lenta' in login or '@autorambler' in login or '@ro' in login:
            # Подключение к серверу IMAP
            mail = imaplib.IMAP4_SSL("imap.rambler.ru")
            # print('rambler')

        else:
            mail = imaplib.IMAP4_SSL("imap.mail.ru")

        mail.login(email_user, email_pass)

        # Выбор почтового ящика
        if count%2 == 0:
            mail.select("inbox")

            # Поиск писем с определенной темой
            typ, msgnums = mail.search(None, 'SUBJECT "Verify your Layer3 email"')
            msgnums = msgnums[0].split()

            # Обработка писем
            link = ''

            for num in msgnums:
                typ, data = mail.fetch(num, "(BODY[TEXT])")
                msg = email.message_from_bytes(data[0][1])
                text = msg.get_payload(decode=True).decode()

                print(text.replace('=\r\n', '').split('<a href=3D"')[1].split('" target=3D"')[0])

                print(text)
                input()

                # Поиск ссылки в тексте письма
                link_pattern = r'https://trove-api.treasure.lol/account/verify-email\S*'
                match = re.search(link_pattern, text.replace('=\r\n', '').replace('"', ' '))

                # ('\n\printn')
                if match:
                    link = match.group().replace("verify-email?token=3D", "verify-email?token=").replace("&email=3D", "&email=").replace("&redirectUrl=3D", "&redirectUrl=")
                    # print(f"Найдена ссылка: \n\n{link}")
                else:
                    # print("Ссылка не найдена")
                    count += 1
                    time.sleep(2)

            # Завершение сессии и выход
            mail.close()
            mail.logout()

            if link != '':
                return link
        else:
            mail.select("Spam")

            # Поиск писем с определенной темой
            typ, msgnums = mail.search(None, 'SUBJECT "Verify your Layer3 email"')
            msgnums = msgnums[0].split()

            # Обработка писем
            link = ''

            for num in msgnums:
                typ, data = mail.fetch(num, "(BODY[TEXT])")
                msg = email.message_from_bytes(data[0][1])
                text = msg.get_payload(decode=True).decode()

                # print(text.replace('=\r\n', '').split('<a href=3D"')[1].split('" target=3D"')[0])



                # Поиск ссылки в тексте письма
                link_pattern = r'https://layer3.xyz/verify-email\S*'
                match = re.search(link_pattern, text.replace('=\r\n', '').replace('"', ' '))

                # ('\n\printn')
                if match:
                    print(text.replace('=\r\n', '').split('<a href=3D"')[1].split('"')[0])
                    link = text.replace('=\r\n', '').split('<a href=3D"')[1].split('"')[0]
                    # print(f"Найдена ссылка: \n\n{link}")
                else:
                    # print("Ссылка не найдена")
                    count += 1
                    time.sleep(2)

            # Завершение сессии и выход
            mail.close()
            mail.logout()

            if link != '':
                return link

    return None

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_random_code():
    code = ''
    for _ in range(32):
        code += random.choice(string.hexdigits[:-6])
    return code

class DeBank:

    def __init__(self, accs_data):

        # self.id = id
        # self.cap_key = cap_key
        self.address = accs_data['address'].lower()
        self.private_key = accs_data['private_key']
        # self.tw_auth_token = accs_data['tw_auth_token']
        # self.tw_csrf = accs_data['tw_csrf']
        # self.discord_token = accs_data['discord_token']
        # self.mail = accs_data['mail']
        # self.mail_pass = accs_data['mail_pass']


        self.proxy = {'http': accs_data['proxy'], 'https': accs_data['proxy']}
        self.static_sitekey = '6LddBO8eAAAAAEH9BqJaGJ-vMnO4_Sp8-TQ36RLl'

        self.session = self._make_scraper()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.proxies = self.proxy

        self.code = generate_random_code()
        # print(self.code)
        ua = ua_generator.generate(platform="windows").text
        self.ts = int(datetime.utcnow().timestamp())
        self.session.headers.update({'Content-Type': 'application/json',
                                     'Accept': '*/*',
                                     'Account': f'{{"random_at":{self.ts},"random_id":{self.code},"user_addr":null}}',
                                     'User-Agent':ua,
                                     'X-Api-Ver': 'v2',

                                     })
        self.session.user_agent = ua


        # print(self.session.user_agent)

        # with self.session.get('https://layer3.xyz/quests', timeout=10) as response:
        #     print(response.text)
        #     pass

    def GetNonce(self):


        payload = {"id": self.address}

        with self.session.post('https://api.debank.com/user/sign_v2', json=payload, timeout=30) as response:
            # print(response.text)
            # return response.json()[0]['result']['data']['json']
            return response.json()['data']['text']

    def Authorize(self):

        self.nonce = self.GetNonce()

        # print(f'Layer3 One-Time Key: {self.nonce}')

        message = encode_defunct(text=self.nonce)
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        self.signature = signed_message["signature"].hex()


        payload = {"signature": self.signature, "id": self.address}

        # print(payload)
        time.sleep(random.randint(200, 800) / 100)
        self.session.headers.update({'X-Api-Ts': str(datetime.utcnow().timestamp())})
        with self.session.post('https://api.debank.com/user/login_v2', json=payload, timeout=30) as response:
            print(response.text)

            if response.json()['error_code'] == 400:


                # print(payload)
                time.sleep(random.randint(200, 800) / 100)
                payload = {"signature": self.signature, "id": self.address, "token": self.CaptchaSolver()}
                self.session.headers.update({'X-Api-Ts': str(datetime.utcnow().timestamp())})
                with self.session.post('https://api.debank.com/user/login_v2', json=payload, timeout=30) as response:
                    print(response.text)

                    self.id = response.json()['data']['session_id']

                    self.session.headers.update({'Account': f'{{"random_at": {self.ts}, "random_id": "{self.code}", "session_id": "{self.id}", "user_addr": "{self.address}", "wallet_type": "metamask", "is_verified": true}}'})

            else:
                self.id = response.json()['data']['session_id']

                self.session.headers.update({'Account': f'{{"random_at": {self.ts}, "random_id": "{self.code}", "session_id": "{self.id}", "user_addr": "{self.address}", "wallet_type": "metamask", "is_verified": true}}'})



    def CaptchaSolver(self):

        from capmonster_python import RecaptchaV2Task

        capmonster = RecaptchaV2Task("0489ea3764a5bf95bc957da8d7861ed1")
        task_id = capmonster.create_task("https://debank.com/",
                                         "6LfoubcmAAAAAOa4nrHIf2O8iH4W-h91QohdhXTf")
        result = capmonster.join_task_result(task_id)
        # print(result.get("gRecaptchaResponse"))
        return result.get("gRecaptchaResponse")

    def GetStats(self):

        with self.session.get(f'https://api.debank.com/user?id={self.address}', timeout=30) as response:
            print(self.address, response.json()['data']['user']['desc']['is_spam'])

            resp = response.json()['data']['user']

            return resp['follower_count'], resp['following_count'], resp['rank_at'], resp['stats']['usd_value'], resp['tvf']

    def Repost(self, id):

        payload = {'id': id}

        with self.session.post('https://api.debank.com/article/repost', json=payload) as response:
            return response.json()

    def Comment(self, id, text):

        payload = {'id': id,
                   'content': text}

        with self.session.post('https://api.debank.com/article/comment', json=payload) as response:
            return response.json()

    def Follow(self, address):

        # print(self.session.headers)
        self.session.headers.update({'X-Api-Ts': str(datetime.utcnow().timestamp())})
        with self.session.get(f'https://api.debank.com/user/follow?addr={address}', timeout=15) as response:
            print(response.text)
            pass
    def MakePost(self, text, images=None):
        # print(images)
        self.session.headers.update({"content-type": "application/json"})
        if images == None:
            with self.session.post('https://api.debank.com/article/add', json={"content":text}, timeout=15) as response:
                # print(response.text)
                pass
        else:
            with self.session.post('https://api.debank.com/article/add', json={"content": text,"entities":{},"image_ids":images},
                                   timeout=15) as response:
                # print(response.text)
                pass
            return 0

    def UploadImage(self, path):

        c = generate_random_string()

        with open(path, 'rb') as f:
            data = f.read()

        boundary = "------WebKitFormBoundary{0}".format(c).encode('utf-8')
        body = [
            boundary,
            b'Content-Disposition: form-data; name="file"; filename="image.jpeg"',
            b'Content-Type: image/jpeg',
            b'',
            data,
            boundary,
            b'Content-Disposition: form-data; name="category"',
            b'',
            b'feed',
            boundary + b'--'
        ]
        body_data = b'\r\n'.join(body)

        self.session.headers.update({'content-type': 'multipart/form-data; boundary={0}'.format(
            boundary.decode('utf8')[2:]
        )})

        with self.session.post('https://api.debank.com/common/upload_image_v2', data=body_data, timeout=60) as response:
            # print(response.json())
            return response.json()['data']['image']['id']

    def ShowMyNFT(self):

        with self.session.get(f'https://api.debank.com/nft/list?is_collection=1&user_addr={self.address}') as response:
            return response.json()

    def UpdateLogo(self, nft_id, chain_id):

        payload = {"chain_id":chain_id,
                   "nft_id":nft_id}

        with self.session.post('https://api.debank.com/user/update_logo', json=payload) as response:
            # print(response.json())
            return response.json()

    def JoinLuckyDraw(self, id):

        payload = {'id': id}

        self.session.headers.update({'X-Api-Ts': str(datetime.utcnow().timestamp())})
        with self.session.post('https://api.debank.com/feed/draw/join', json=payload) as response:
            print(response.text)
            return response.json()


    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )

if __name__ == '__main__':

    addresses = []
    privates = []
    proxys = []

    with open('Data/Address.txt', 'r') as file:
        for i in file:
            addresses.append(i.rstrip())

    with open('Data/Privates.txt', 'r') as file:
        for i in file:
            privates.append(i.rstrip())

    with open('Data/Proxy.txt', 'r') as file:
        for i in file:
            proxys.append(i.rstrip())

    list_ = []
    for i in range(len(addresses)):
        list_.append([addresses[i], privates[i], proxys[i]])

    random.shuffle(list_)

    for i in range(len(list_)):

        try:
            DB_Account = DeBank({'address': list_[i][0],
                                 'private_key': list_[i][1],
                                 'proxy': f'http://{list_[i][2].split(":")[2]}:{list_[i][2].split(":")[3]}@{list_[i][2].split(":")[0]}:{list_[i][2].split(":")[1]}'})

            DB_Account.Authorize()
            DB_Account.GetStats()
        except:
            # traceback.print_exc()
            # input()
            print(addresses[i], 'ошибка')










    DB_Account = DeBank({'address':'0xbd871b72fe3c77ab91a394744319e3ca325f8997',
            'private_key':'0x3b12db1218de7148d32547320968414088f806df7584ebcd5dbd6a0174de3bd2',
            'proxy':'http://wnfefygv:cw1tbwmm3mdn@156.238.9.101:6992'})

    DB_Account.Authorize()
    time.sleep(4)
    # DB_Account.Follow('0xcedafb4137505a23238e225378293e6c0fde1745')
    data = DB_Account.ShowMyNFT()

    all_nfts = []
    for i in data['data']['collection_dict']:
        all_nfts.append(str(i))

    nft_id = None
    randomNFT = random.choice(all_nfts)
    for i in data['data']['token_list']:
        if i['collection_id'] == randomNFT:
            nft_id = i['id']
            break

    time.sleep(4)
    DB_Account.UpdateLogo(nft_id,randomNFT.split(':')[0])
    # DB_Account.JoinLuckyDraw(3539)

    # imgs = [DB_Account.UploadImage(r"C:\Users\User\Downloads\водопад.jpeg")]
    # DB_Account.MakePost('Look at this', imgs)
