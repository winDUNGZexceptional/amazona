from django.core.exceptions import ValidationError
import re

from apps.users.models import User



def name_validation(name):
	# this is a regex pattern r that says this is a raw string
	# [] says that this a group of string.
	# ^ after a opening square bracket is to say this is excepted.
	# ^a-zA-Z\. means that \. (period only. \ is to say that this is a string)
	# letters of lower case a-z and upper case A-Z and periods are excepted.

	# split the name to avoid double spaces.
	# if i != '' means that it will not accept double spaced words.
	pattern = r"[^a-zA-Z\.]+"
	splitted_name = [i for i in name.split(' ') if i != '']

	counter = 0

	# re.search is a regex function that search the string if it matches the pattern
	# if there is a number or other characters (which is not excepted) is found,
	# it will return an error message not the success.
	for name in splitted_name:
		if re.search(pattern, name):
			counter += 1

	if counter > 0:
		raise ValidationError(
			"Name should not contain special characters and numbers"
			)



def alias_validation(alias):
	pattern = r"[^a-zA-Z0-9\.\-\_]+"

	if re.search(pattern, alias):
		raise ValidationError(
			"Alias should not contain special characters \
			other than underscore, period, and hyphen"
			)



def unique_alias_validation(alias):

	alias_exists = User.objects.filter(alias = alias).exists()

	if alias_exists:
		raise ValidationError("Alias already exists.")



def email_validation(email):
	# --------------------------------------------------------------------

	# in this regex this can be interpreted as
	# string starts ^ with a group [] of alphanumeric characters \w
	# can have + - . that can repeat at least once.
	# have an @ sign and proceed with a group of alphanumeric and dashes
	# at least once +
	# with period after it then group of string again at the end $

	# --------------------------------------------------------------------
	pattern = r"(^[\w\.\+\-]+@[\w\-]+\.[\w\-\.]+$)"

	if not re.search(pattern, email):
		raise ValidationError("Email is not a valid email")


def unique_email_validation(email):

	email_exists = User.objects.filter(email=email).exists()

	if email_exists:
		raise ValidationError("Email address already exists.")