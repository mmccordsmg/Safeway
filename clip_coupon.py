import argparse
from safeway_funcs import safeway_login, safeway_get_preferred_store, safeway_clip_coupons

parser = argparse.ArgumentParser(description="Logs in with the given username and password. Clips specific coupon")
parser.add_argument("-u",	"--username",	help="Username",											required=True,	type=str)
parser.add_argument("-p",	"--password",	help="Password",											required=True,	type=str)
parser.add_argument("-c",	"--coupon",		help="Personalized coupon to clip",		required=True,	type=str)

args = parser.parse_args()

token = safeway_login(args.username, args.password)
if token:
	mystore = safeway_get_preferred_store(token)
	coupons = []
	coupons.append({"offerId": args.coupon, "offerPgm": "MF"})
	safeway_clip_coupons(coupons, mystore, token)
else:
	print("Login Failed!")
