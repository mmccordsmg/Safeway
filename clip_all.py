import argparse
from safeway_funcs import safeway_login, safeway_get_coupons, safeway_get_preferred_store, safeway_clip_coupons

parser = argparse.ArgumentParser(description="Logs in with the given username and password. Clips all coupons on account.")
parser.add_argument("-u",	"--username",	help="Username",				required=True,	type=str)
parser.add_argument("-p",	"--password",	help="Password",				required=True,	type=str)
args = parser.parse_args()

token = safeway_login(args.username, args.password)
if token:
	mystore = safeway_get_preferred_store(token)
	coupons = safeway_get_coupons(mystore, token)
	if coupons:
		safeway_clip_coupons(coupons, mystore, token)
	else:
		print("Error getting coupon list, or no coupons to clip!")
else:
	print("Login Failed!")
