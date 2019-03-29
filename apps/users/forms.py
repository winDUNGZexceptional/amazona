from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django import forms

from apps.users.validators import name_validation, alias_validation
from apps.users.validators import unique_email_validation, email_validation
from apps.users.validators import unique_alias_validation




class RegisterForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

	name = forms.CharField(
		min_length = 4,
		max_length = 255, 
		required = True,
		validators = [name_validation,]
		)

	alias = forms.CharField(
		min_length = 5,
		max_length = 255, 
		required = True,
		validators = [alias_validation, unique_alias_validation,]
		)

	email = forms.CharField(
		max_length = 255, 
		required = True,
		validators = [email_validation, unique_email_validation,]
		)

	password = forms.CharField(
		min_length = 8,
		max_length = 40,
		required = True,
		widget = forms.PasswordInput,
		help_text = 'Password should be more than 8 characters'
		)

	confirm_password = forms.CharField(
		min_length = 8,
		max_length = 40,
		required = True,
		widget = forms.PasswordInput,
		help_text = 'Should be the same as your password'
		)



	def clean_confirm_password(self):
		password1 = self.cleaned_data.get('password', None)
		password2 = self.cleaned_data.get('confirm_password', None)

		if password1 != password2:
			raise ValidationError("Passwords do not match.")

		else:
			encrypted_password = make_password(password2)
			print(encrypted_password)
			return encrypted_password



class LoginForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'


	email = forms.CharField(
		max_length = 255,
		required = True
		)

	password = forms.CharField(
		widget = forms.PasswordInput,
		required = True
		)