import argparse
from safeway_funcs import safeway_login, safeway_get_coupons, safeway_get_preferred_store, safeway_clip_coupons

parser = argparse.ArgumentParser(description="Logs in with the given username and password. Clips all coupons on account.")
parser.add_argument("-u",	"--username",	help="Username",				required=True,	type=str)
parser.add_argument("-p",	"--password",	help="Password",				required=True,	type=str)
args = parser.parse_args()

token = safeway_login(args.username, args.password)
if token:
	mystore = safeway_get_preferred_store(token)
	coupons = safeway_get_coupons(mystore, token, "personalized")
	if coupons:
		safeway_clip_coupons(coupons, mystore, token, "personalized")
	else:
		print("Error getting personalized coupon list!")
	coupons = safeway_get_coupons(mystore, token, "manufacturer")
	if coupons:
		safeway_clip_coupons(coupons, mystore, token, "manufacturer")
	else:
		print("Error getting manufacturer coupon list!")
else:
	print("Login Failed!")
