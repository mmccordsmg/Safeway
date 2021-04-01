import requests
import json
import jwt
from datetime import datetime
import uuid
from time import sleep

session = requests.Session()
session.verify = False
session.proxies = { 'https': 'http://127.0.0.1:8080' }

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def safeway_login (username, password):
	global session
	loginurl='https://albertsons.okta.com/api/v1/authn'
	session.headers.update(
		{
				"user-agent": "Safeway/7957 CFNetwork/1220.1 Darwin/20.3.0", 
				"content-type": "application/json",
				"accept": "application/json",
				"adrum_1": "isMobile:true",
				"adrum": "isAjax:true"
		}
	)
	payload={ "password": password, "username": username }
	r=session.post(loginurl, data=json.dumps(payload))
	if r.json().get("sessionToken"):
		session.headers.update(
			{
				"authorization": 'Basic MG9hcDZra3A3U2VmZzI0ckIycDY6NFVwbXpENGhsRjJWWVFxWWpEVW9hbWdMdTJCbzFPemFncGZHN3l1cw==',
				'content-type': 'application/x-www-form-urlencoded'
			}
		)
		payload = {
			'username': username,
			'password': password,
			'grant_type': 'password',
			'scope': 'openid profile offline_access'
		}
		r = session.post('https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/token', data=payload)
		if r.json().get('access_token'):
			return(r.json()["access_token"])
		else:
			return(False)
	else:
		return(False)

def safeway_get_store_information(storenumber):
	global session
	session.headers.update(
		{
				"User-Agent": "iphone", 
				"Content-Type": "application/vnd.safeway.v1+json;charset=UTF-8",
				"Accept": "application/vnd.safeway.v1+json",
				"X-IBM-Client-Secret": "Q8hD5aP8nU6mL6nC0yB6xC5lS0mP3lQ7fO7mU0qE3xI6oC5fO1",
				"CLIENT_APP_VERSION": "10.2.0",
				"x-swy-client-id": "mobile-ios-portal",
				"X-SWY_API_KEY": "0fdb13ac50972b700f8a9e352d8ea123414ae1f1.safeway.j4u.iphone",
				"X-IBM-Client-Id": "0576e73c-2fcf-43ed-b107-9866827f81b9",
				"x-swy_banner": "safeway",
				"CLIENT_ID": "",
				"X-SWY_VERSION": "1.5",
				'Ocp-Apim-Subscription-Key': 'b2ea4df305624d96960191e1aaed9b9d'
		}
	)
	r = session.get(f'https://www.acmemarkets.com/api/services/locator/entity/store/{storenumber}')
	rjson = r.json()
	if rjson.get('resultCount') == 1:
		store = {}
		store['brand'] = rjson.get('store').get('brand')
		store['division'] = rjson.get('store').get('division')
		store['address'] = rjson.get('store').get('address')
		store['number'] = storenumber
		return(store)
	else:
		#print(f'Error fetching store information for store# {storenumber}')
		#print(r.text)
		return(False)
		
def safeway_get_preferred_store(token):
	global session
	session.headers.update(
		{
				"User-Agent": "iphone", 
				"Content-Type": "application/vnd.safeway.v1+json;charset=UTF-8",
				"Accept": "application/vnd.safeway.v1+json",
				"Authorization": "Bearer %s" % token,
				"X-IBM-Client-Secret": "Q8hD5aP8nU6mL6nC0yB6xC5lS0mP3lQ7fO7mU0qE3xI6oC5fO1",
				"CLIENT_APP_VERSION": "10.2.0",
				"x-swy-client-id": "mobile-ios-portal",
				"X-SWY_API_KEY": "0fdb13ac50972b700f8a9e352d8ea123414ae1f1.safeway.j4u.iphone",
				"X-IBM-Client-Id": "0576e73c-2fcf-43ed-b107-9866827f81b9",
				"x-swy_banner": "safeway",
				"CLIENT_ID": "",
				"X-SWY_VERSION": "1.5",
				'Ocp-Apim-Subscription-Key': '1d8f9e6f8b0d4ce29468d6d82f5847b8'
		}
	)
	gid = jwt.decode(token, options={"verify_signature": False})["gid"]
	while True:
		r=session.get(f'https://www.safeway.com/abs/pub/cnc/ucaservice/api/uca/customers/{gid}/stores')
		mystore=False
		stores = r.json().get("stores")
		if stores:
			for store in stores:
				if store["storePreference"] == "Preferred":
					mystore = store["storeId"]
		if mystore:
			return(mystore)
		sleep(5)

def safeway_get_coupons(mystore, token):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/7957 CFNetwork/1220.1 Darwin/20.3.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"Authorization": "Bearer %s" % token,
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway",
				"ADRUM": "isAjax:true",
				"X-SWY_API_KEY": "emmd",
				"ADRUM_1": "isMobile:true",
				"X-SWY-APPLICATION-TYPE": "native-mobile"
		}
	)
	session.headers.update({'Ocp-Apim-Subscription-Key': ''})
	#print(mystore)
	cookies = {'swyConsumerDirectoryPro': token}
	r=session.get(f'https://www.safeway.com/abs/pub/xapi/offers/companiongalleryoffer?storeId={mystore}', cookies=cookies)
	deals = r.json()["companionGalleryOfferList"]
	if deals:
		#print(deals)
		outcoupons = []
		for deal in deals:
			if deal["status"] == 'U':
				outcoupons.append(deal)
	#print (outcoupons)
	return (outcoupons)


def safeway_get_available_rewards(mystore, token):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/7957 CFNetwork/1220.1 Darwin/20.3.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"Authorization": "Bearer %s" % token,
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway",
				"ADRUM": "isAjax:true",
				"X-SWY_API_KEY": "emmd",
				"ADRUM_1": "isMobile:true",
				"X-SWY-APPLICATION-TYPE": "native-mobile"
		}
	)
	session.headers.update({'Ocp-Apim-Subscription-Key': ''})
	#print(mystore)
	cookies = {'swyConsumerDirectoryPro': token}
	r=session.get(f'https://nimbus.safeway.com/rewards/service/gallery/offer/gr?storeId={mystore}', cookies=cookies)
	deals = r.json()["grOffers"]
	if deals:
		#print(deals)
		outcoupons = []
		for deal in deals:
			if deal["status"] == 'U':
				outcoupons.append(deal)
	#print (outcoupons)
	return (outcoupons)

def safeway_get_clipped_rewards(mystore, token):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/7957 CFNetwork/1220.1 Darwin/20.3.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"Authorization": "Bearer %s" % token,
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway",
				"ADRUM": "isAjax:true",
				"X-SWY_API_KEY": "emmd",
				"ADRUM_1": "isMobile:true",
				"X-SWY-APPLICATION-TYPE": "native-mobile"
		}
	)
	session.headers.update({'Ocp-Apim-Subscription-Key': ''})
	#print(mystore)
	cookies = {'swyConsumerDirectoryPro': token}
	r=session.get(f'https://www.acmemarkets.com/abs/pub/web/j4u/api/grocery/rewards/mylist?storeId={mystore}', cookies=cookies)
	deals = r.json()["myGroceryRewardsList"]
	if deals:
		#print(deals)
		outcoupons = []
		for deal in deals:
			if deal["status"] == 'U':
				outcoupons.append(deal)
	#print (outcoupons)
	return (outcoupons)

def safeway_clip_coupons(coupons, mystore, token):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/7957 CFNetwork/1220.1 Darwin/20.3.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway",
				"ADRUM": "isAjax:true",
				"X-SWY_API_KEY": "0fdb13ac50972b700f8a9e352d8ea123414ae1f1.acmemarkets.j4u.iphone",
				"ADRUM_1": "isMobile:true",
				"Ocp-Apim-Subscription-Key": ""
		}
	)
	cookies = {'swyConsumerDirectoryPro': token}
	url=f"https://nimbus.safeway.com/Clipping1/services/clip/items?storeId={mystore}"
	while len(coupons):
		i=0
		toclip=[]
		while (len(coupons) and i<125):
			coupon = coupons.pop()
			toclip.append(
				{
						"clipType": "C",
						"itemId": coupon["offerId"],
						"itemType": coupon["offerPgm"]
				}
			)
			toclip.append(
				{
						"clipType": "L",
						"itemId": coupon["offerId"],
						"itemType": coupon["offerPgm"]
				}			
			)
			i+=1
		payload={"items": toclip}
		r=session.post(url, data=json.dumps(payload), cookies=cookies)
		print(f'Clipping {len(toclip)/2:.0f} coupons')
		#print(r.text)
	return(True)

def safeway_clip_rewards(rewards, mystore, token):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/7957 CFNetwork/1220.1 Darwin/20.3.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway",
				"ADRUM": "isAjax:true",
				"X-SWY_API_KEY": "0fdb13ac50972b700f8a9e352d8ea123414ae1f1.acmemarkets.j4u.iphone",
				"ADRUM_1": "isMobile:true",
				"Ocp-Apim-Subscription-Key": ""
		}
	)
	cookies = {'swyConsumerDirectoryPro': token}
	url=f"https://nimbus.safeway.com/Clipping1/services/clip/items?storeId={mystore}"
	while len(rewards):
		i=0
		toclip=[]
		while (len(rewards) and i<125):
			reward = rewards.pop()
			toclip.append(
				{
						"clipType": "C",
						"itemId": reward["offerId"],
						"itemType": reward["offerPgm"],
						"vndrBannerCd": None
				})
			i+=1
		payload={"items": toclip}
		print(f'Clipping {len(toclip):.0f} rewards')
		r=session.post(url, data=json.dumps(payload), cookies=cookies)
		itms = r.json().get('items')
		for item in itms:
			if item.get('status'):
				print(f'{item.get("itemId")}: Successfully clipped')
			else:
				print(f'{item.get("itemId")}: {item.get("errorMsg")}')
		#print(r.text)
	return(True)

def safeway_unclip_rewards(rewards, mystore, token):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/7957 CFNetwork/1220.1 Darwin/20.3.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway",
				"ADRUM": "isAjax:true",
				"X-SWY_API_KEY": "0fdb13ac50972b700f8a9e352d8ea123414ae1f1.acmemarkets.j4u.iphone",
				"ADRUM_1": "isMobile:true",
				"Ocp-Apim-Subscription-Key": ""
		}
	)
	cookies = {'swyConsumerDirectoryPro': token}
	url=f"https://nimbus.safeway.com/Clipping1/services/update/items?storeId={mystore}"
	while len(rewards):
		i=0
		toclip=[]
		while (len(rewards) and i<125):
			reward = rewards.pop()
			toclip.append(
				{
						"id": reward["offerId"],
						"checked": "true",
						"itemType": reward["offerPgm"],
						"storeId": mystore
				}
			)
			i+=1
		payload={"items": toclip}
		print(f'Unclipping {len(toclip):.0f} rewards')
		r=session.post(url, data=json.dumps(payload), cookies=cookies)
		itms = r.json().get('items')
		for item in itms:
			if item.get('status'):
				print(f'{item.get("itemId")}: Successfully clipped')
			else:
				print(f'{item.get("itemId")}: {item.get("errorMsg")}')
		#print(r.text)
	return(True)

def safeway_create_account(email, password, firstname, lastname, phone, preferredstore, zipcode):
	global session
	session.headers.update(
		{
					"content-type": "application/vnd.safeway.v1+json;charset=UTF-8",
					"x-swy_banner": "safeway",
					"accept": "application/vnd.safeway.v1+json",
					"x-ibm-client-id": str(uuid.uuid4()),
					"client_app_version": "10.2.0",
					"x-swy-client-id": "mobile-ios-portal",
					"x-swy_api_key": "0fdb13ac50972b700f8a9e352d8ea123414ae1f1.safeway.j4u.iphone",
					"user-agent": "iphone",
					"x-swy_version": "1.5",
					"x-swy-correlation-id": str(uuid.uuid4()),
					"x-swy-date": datetime.now().strftime("%a, %d %b %Y %H:%M:%S"),
					"ocp-apim-subscription-key":	"1d8f9e6f8b0d4ce29468d6d82f5847b8"
		}
	)
	url = 'https://www.safeway.com/abs/pub/cnc/ucaservice/api/uca/customers/register'
	payload = {
				"firstName": firstname,
				"digitalReceipt": "N",
				"preferences": {
						"stores": [
								{
										"storePreference": "Preferred",
										"storeId": preferredstore
								}
						],
				"emailOffers": "Y"
				},
				"terms": "true",
				"password": password,
				"lastName": lastname,
				"phone": [
						{
								"type": "mobile",
								"number": phone
						}
				],
			"zipCode": zipcode,
			"emailId": email,
			"userId": email,
			"clubCardNumber": ""
	}
	r=session.post(url, data=json.dumps(payload))
	return(r.json().get("customerId"), r.json().get("clubCardNumber"), r.json().get("errors"))

def safeway_clip_all_coupons(username, password, mystore=None):
	token = safeway_login(username, password)
	if token:
		if not mystore:
			mystore = safeway_get_preferred_store(token)
		coupons = safeway_get_coupons(mystore, token)
		if coupons:
			safeway_clip_coupons(coupons, mystore, token)
		else:
			print("Error getting coupon list!")
	else:
		print("Login Failed!")