from django import forms
from django.core.exceptions import ValidationError

from apps.books.models import Author
from apps.books.validators import unique_author, unique_title, author_name_validation
from apps.books.validators import author_name_validation


class AddBookForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(AddBookForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

	title = forms.CharField(
		min_length = 5,
		max_length = 255,
		required = True,
		validators = [unique_title,]
		)

	summary = forms.CharField(
		min_length = 50,
		widget = forms.Textarea
		)



class AddAuthorForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(AddAuthorForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

	authors = forms.ModelMultipleChoiceField(
		required = False,
		# widget = forms.CheckboxSelectMultiple,
		queryset = Author.objects
		)

	add_new_author = forms.CharField(
		required = False,
		min_length = 5,
		max_length = 255,
		validators = [unique_author, author_name_validation]
		)


	def clean_add_new_author(self):

		authors = self.cleaned_data.get('authors')
		new_author = self.cleaned_data.get('add_new_author')

		if len(authors) == 0 and new_author == '':
			raise ValidationError('Please add a new author or select existing authors.')
		else:
			return new_author


class AddReviewForm(forms.Form):

	def __init__(self, *args, **kwargs):
		super(AddReviewForm, self).__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

	user = forms.CharField(
		widget = forms.TextInput(attrs = {'readonly' : 'readonly'})
		)

	subject = forms.CharField(
		min_length = 5,
		max_length = 255,
		required = True
		)

	comment = forms.CharField(
		min_length = 15,
		required = True,
		widget = forms.Textarea
		)

	rating = forms.IntegerField(
		help_text = 'Rating ranges from 1 to 5.'
		)


	def clean_rating(self):

		rating = self.cleaned_data.get('rating', None)

		if rating is not None:

			if int(rating) in [1, 2, 3, 4, 5]:
				return rating

			else:
				raise ValidationError('Your rating is too high/low.')

		else:
			raise ValidationError('Please rate the book from 1 - 5.')