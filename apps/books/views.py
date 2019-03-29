from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.books.forms import AddBookForm, AddReviewForm, AddAuthorForm
from apps.users.models import User
from apps.books.models import Book, Review, Author

# Create your views here.


def book_list(request):

	books = Book.objects.all()

	other_books = [book for book in books if len(book.review_set.all()) > 0]

	latest_book_reviews = sorted(
		other_books,
		key = lambda book: book.review_set.last().date_created,
		reverse = True
		)

	context = {
	'books' : latest_book_reviews[:3],
	'other_books' : other_books,
	}
	return render(request, 'books/pages/list.html', context)


def add_book(request):

	if 'user' not in request.session:
		messages.error(request, 'Login first before giving a review.')
		return HttpResponseRedirect( reverse('users:index') )

	user_alias = request.session['user']['alias']
	
	book_form = AddBookForm()
	review_form = AddReviewForm(initial = {'user' : user_alias})
	author_form = AddAuthorForm()

	context = {
	'book_form' : book_form,
	'review_form' : review_form,
	'author_form' : author_form,
	}
	return render(request, 'books/pages/add.html', context)


def create_book(request):

	if 'user' not in request.session:
		messages.error(request, 'You are not yet logged in.')
		return HttpResponseRedirect( reverse('users:index') )
	
	if request.method == 'POST':
		
		book_form = AddBookForm(request.POST)
		review_form = AddReviewForm(request.POST)
		author_form = AddAuthorForm(request.POST)

		user = User.objects.filter(
			email = request.session['user']['email']
			).first()

		number_of_errors = 0

		if book_form.is_valid():
			print('book pass!')

			new_book = Book.objects.create(
				title = book_form.cleaned_data.get('title'),
				summary = book_form.cleaned_data.get('summary')
				)

		else:
			print(book_form.errors)
			messages.error(request, book_form.errors)
			number_of_errors += 1

			return HttpResponseRedirect( reverse('books:add') )


		if review_form.is_valid():
			print('review pass!')

			new_review = Review.objects.create(
				user = user,
				book = new_book,
				subject = review_form.cleaned_data.get('subject'),
				comment = review_form.cleaned_data.get('comment'),
				rating = review_form.cleaned_data.get('rating')
				)


		else:
			print(review_form.errors)
			messages.error(request, review_form.errors)
			number_of_errors += 1

			new_book.delete()

			return HttpResponseRedirect( reverse('books:add') )


		if author_form.is_valid():
			print('author pass!')

			new_author = author_form.cleaned_data.get('add_new_author', None)
			existing_authors = author_form.cleaned_data.get('authors', None)

			if new_author is not None and new_author.replace(' ', '') != '':

				added_author = Author.objects.create(
					name = new_author
					)

				new_book.author_set.add(added_author)
				

			if existing_authors is not None and len(existing_authors) != 0:

				for i in existing_authors:
					new_book.author_set.add(i)

				print('Authors added to the new book.')

		else:
			print(author_form.errors)
			messages.error(request, author_form.errors)
			number_of_errors += 1

			new_book.delete()
			new_review.delete()

			return HttpResponseRedirect( reverse('books:add') )


		if number_of_errors > 0:
			messages.error(request, 'Failed to validate entries due to error.')
			return HttpResponseRedirect( reverse('books:add') )

		else:
			messages.success(request, 'Creation complete!')
			return HttpResponseRedirect( reverse('books:show', args=(new_book.id,)) )


	else:
		messages.error(request, 'You are not allowed to this page.')
		return HttpResponseRedirect( reverse('books:add') )




def show_book(request, book_id):

	book = Book.objects.filter(id = book_id).first()

	if book is not None:

		if 'user' in request.session:
			user_alias = request.session['user']['alias']
			review_form = AddReviewForm(initial={'user' : user_alias})

		else:
			user_alias = None
			review_form = None

		total_rating = 0

		reviews = book.review_set.all()

		for review in reviews:
			total_rating += review.rating

		try:
			total_rating /= len(reviews)
		except ZeroDivisionError:
			total_rating = 'Not yet rated.'

		context = {
		'book' : book,
		'reviews' : reviews,
		'total_rating' : total_rating,
		'review_form' : review_form,
		}
		return render(request, 'books/pages/show.html', context)

	else:
		messages.error(request, 'Invalid book ID.')
		return HttpResponseRedirect( reverse('books:list') )



def delete_review(request, book_id, review_id):

	if 'user' in request.session:

		review = Review.objects.filter(id = review_id).first()
		user_id = request.session['user']['id']

		if review.user.id == user_id:
			
			review.delete()
			messages.success(request, 'You have successfully deleted your review.')
			return HttpResponseRedirect( reverse('books:show', args=(book_id,)) )

		else:
			messages.error(request, 'You are not the owner of this review.')
			return HttpResponseRedirect( reverse('books:show', args=(book_id,)) )


	else:
		messages.error(request, 'Please login first before accessing this link.')
		return HttpResponseRedirect( reverse('users:index') )



def add_review(request, book_id):

	if request.method == 'POST':

		if 'user' in request.session:

			review_form = AddReviewForm(request.POST)

			if review_form.is_valid():

				user = User.objects.filter(
					alias = review_form.cleaned_data.get('user')
					).first()

				book = Book.objects.filter(id = book_id).first()
				
				new_review = Review.objects.create(
					user = user,
					book = book,
					subject = review_form.cleaned_data.get('subject'),
					comment = review_form.cleaned_data.get('comment'),
					rating = review_form.cleaned_data.get('rating')
					)

				messages.success(request, 'Review creation success!')
				return HttpResponseRedirect( reverse('books:show', args=(book_id,)))

			else:
				messages.error(review_form.errors)
				return HttpResponseRedirect( reverse('books:show', args=(book_id,)))

		else:
			messages.error(request, 'Please login first before accessing this link.')
			return HttpResponseRedirect( reverse('books:show', args=(book_id,)))

	else:
		messages.error(request, 'You are not allowed here.')
		return HttpResponseRedirect( reverse('books:show', args=(book_id,)) )