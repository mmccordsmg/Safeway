import argparse
from safeway_funcs import safeway_create_account, safeway_clip_all_coupons

parser = argparse.ArgumentParser(description="Batch creates safeway accounts.  Prints the customer id/card# if successful.  Clips all coupons in requested.")
parser.add_argument("-e",	"--emailprefix",	help="Email prefix.  Will be appended by a 3 digit zero-padded number and the specified suffix.", required=True,	type=str)
parser.add_argument("-x",	"--emailsuffix",	help="Email suffix.  This is the part after the zero-padded 3 digit number.", required=True,	type=str)
parser.add_argument("-p",	"--password",	help="Password",								required=True,	type=str)
parser.add_argument("-f",	"--firstname",	help="First Name",						required=True,	type=str)
parser.add_argument("-l",	"--lastname",	help="Last Name",								required=True,	type=str)
parser.add_argument("-o",	"--phoneprefix",	help="Phone Number prefix.  7 numbers.  No parentheses or dashes.",	required=True,	type=int)
parser.add_argument("-s",	"--storenumber",	help="Preferred Store #",		required=False,	type=str, default='4030')
parser.add_argument("-z",	"--zipcode",	help="Zip Code",								required=False,	type=str, default='19702')
parser.add_argument("-t",	"--startnumber",	help="Number to start from.", required=True, type=int)
parser.add_argument("-n",	"--endnumber",	help="Number to end on.",	required=True,	type=int)
parser.add_argument("-c",	"--clipcoupons",	help="Clip coupons on new accounts", required=False, action='store_true')


args = parser.parse_args()

if len(str(args.phoneprefix)) != 7:
	print("Phone prefix must be 7 numeric digits")
	exit()
if (args.endnumber - args.startnumber) > 1000:
	print("Maximum 1000 accounts per run.")
	exit()
	
if (args.endnumber - args.startnumber) <=0:
	print("startnumber must be less than endnumber")
	exit()

for i in range(args.startnumber, args.endnumber):
	email=args.emailprefix + str(i).zfill(3) + args.emailsuffix
	if "@" not in email:
		print("email prefix and suffix do not create valid email address")
		exit()
	phone=str(args.phoneprefix) + str(i).zfill(3)
	customerid, clubcardnumber, errors = safeway_create_account(email, args.password, args.firstname, args.lastname, phone, args.storenumber, args.zipcode)
	if not customerid:
		print(f"Error creating account {email}")
		print(f"Errors: {errors}")
	else:
		if not clubcardnumber:
			print(f"Account already existed! Email: {email}, Customer id: {customerid}, Phone: {phone}")
			if args.clipcoupons:
				print(f"Clipping coupons on {email}")
				safeway_clip_all_coupons(email, args.password, mystore=args.storenumber)
		else:
			print(f"Account successfully created! Email: {email}, Customer id: {customerid}, Card number: {clubcardnumber}, Phone: {phone}")
			if args.clipcoupons:
				print(f"Clipping coupons on {email}")
				safeway_clip_all_coupons(email, args.password, mystore=args.storenumber)