from django.core.exceptions import ValidationError

from apps.books.models import Author, Book



def unique_author(author_name):

	author_exists = Author.objects.filter(name = author_name).exists()

	if author_exists:
		raise ValidationError('Author already exists.')


def unique_title(book_title):

	title_exists = Book.objects.filter(title = book_title).exists()

	if title_exists:
		raise ValidationError('Title already exists.')


def author_name_validation(author_name):
	if author_name != '':
		if author_name.replace(' ', '') == '':
			raise ValidationError('Author name is not valid.')