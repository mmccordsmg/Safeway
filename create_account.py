import argparse
from safeway_funcs import safeway_create_account

parser = argparse.ArgumentParser(description="Attempts to create a safeway account.  Prints the customer id/card# if successful.")
parser.add_argument("-e",	"--email",	help="Email",											required=True,	type=str)
parser.add_argument("-p",	"--password",	help="Password",								required=True,	type=str)
parser.add_argument("-f",	"--firstname",	help="First Name",						required=True,	type=str)
parser.add_argument("-l",	"--lastname",	help="Last Name",								required=True,	type=str)
parser.add_argument("-o",	"--phone",	help="Phone Number",							required=True,	type=str)
parser.add_argument("-s",	"--storenumber",	help="Preferred Store #",		required=True,	type=str, default='4030')
parser.add_argument("-z",	"--zipcode",	help="Zip Code",								required=True,	type=str, default='19702')

args = parser.parse_args()

customerid, clubcardnumber, errors = safeway_create_account(args.email, args.password, args.firstname, args.lastname, args.phone, args.storenumber, args.zipcode)
if not customerid:
	print("Error creating account")
	print(errors)
else:
	print(f"Email: {args.email}, Customer id: {customerid}, Card number: {clubcardnumber}")