import requests
import json
import jwt

session = requests.Session()

def safeway_login (username, password):
	global session
	loginurl='https://albertsons.okta.com/oauth2/ausp6soxrIyPrm8rS2p6/v1/token'
	session.headers.update(
		{
				"User-Agent": "Safeway/3590 CFNetwork/1107.1 Darwin/19.0.0", 
				"Content-Type": "application/x-www-form-urlencoded",
				"Accept": "application/json",
				"Authorization": "Basic MG9hcDZra3A3U2VmZzI0ckIycDY6NFVwbXpENGhsRjJWWVFxWWpEVW9hbWdMdTJCbzFPemFncGZHN3l1cw=="
		}
	)
	payload={"password": password, "username": username, "grant_type": "password", "scope": "openid profile offline_access"}
	r=session.post(loginurl, data=payload)
	if r.json().get("access_token"):
		return(r.json()["access_token"])
	else:
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
				"CLIENT_APP_VERSION": "7.5.3",
				"x-swy-client-id": "mobile-ios-portal",
				"X-SWY_API_KEY": "0fdb13ac50972b700f8a9e352d8ea123414ae1f1.safeway.j4u.iphone",
				"X-IBM-Client-Id": "0576e73c-2fcf-43ed-b107-9866827f81b9",
				"x-swy_banner": "safeway",
				"CLIENT_ID": "",
				"X-SWY_VERSION": "1.5"
		}
	)
	gid = jwt.decode(token, verify=False)["gid"]
	url = 'https://api-prod.safeway.com/abs/pub/api/uca/customers/%s/stores' % gid
	r=session.get(url)
	mystore=False
	stores = r.json()["stores"]
	for store in stores:
		if store["storePreference"] == "Preferred":
			mystore = store["storeId"]
	return(mystore)

def safeway_get_coupons(mystore, token, coupontype):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/3590 CFNetwork/1107.1 Darwin/19.0.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway"
		}
	)
	cookies = {'swyConsumerDirectoryPro': token}
	if (coupontype == "personalized"):
		url="https://nimbus.safeway.com/emmd/service/gallery/offer/pd?storeId=%s" % mystore
	elif (coupontype == "manufacturer"):
		url="https://nimbus.safeway.com/emmd/service/gallery/offer/mfg?storeId=%s" % mystore
	else:
		return(False)
	r=session.get(url, cookies=cookies)
	if not r.json()["ack"]:
		return(False)
	else:
		if (coupontype == "personalized"):
			return (r.json()["personalizedDeals"])
		elif (coupontype == "manufacturer"):
			return (r.json()["manufacturerCoupons"])

def safeway_clip_coupons(coupons, mystore, token, coupontype):
	global session
	session.headers.update(
		{
				"User-Agent": "Safeway/3590 CFNetwork/1107.1 Darwin/19.0.0",
				"X-SWY_VERSION": "1.1",
				"Content-Type": "application/json",
				"Accept": "*/*",
				"X-SWY_MOBILE_VERSION": "1.0",
				"Accept-Encoding": "gzip, deflate, br",
				"X-SWY_BANNER": "safeway",
				"ADRUM_1": "isMobile:true",
				"ADRUM": "isAjax:true"
		}
	)
	cookies = {'swyConsumerDirectoryPro': token}
	url="https://nimbus.safeway.com/Clipping1/services/clip/items?storeId=%s" % mystore
	toclip=[]
	for coupon in coupons:
		if (coupontype == "personalized"):
			toclip.append(
				{
						"clipType": "C",
						"itemId": coupon["offerID"],
						"itemType": "PD"
				}
			)
			toclip.append(
				{
						"clipType": "L",
						"itemId": coupon["offerID"],
						"itemType": "PD"
				}			
			)
		elif (coupontype == "manufacturer"):
			toclip.append(
				{
						"clipType": "C",
						"itemId": coupon["couponID"],
						"itemType": "SC"
				}
			)
			toclip.append(
				{
						"clipType": "L",
						"itemId": coupon["couponID"],
						"itemType": "SC"
				}			
			)
	payload={"items": toclip}
	r=session.post(url, data=json.dumps(payload), cookies=cookies)
	print(r.text)
	return(True)