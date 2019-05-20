from django.shortcuts import render
from django.http import HttpResponse


posts = [
		{
			'author' : 'Tyler',
			'title' : 'First Post',
			'content' : 'This is my first post',
			'date_posted' : '5/20/2019'
		},
		{
			'author' : 'Sophia',
			'title' : 'My Post',
			'content' : 'This is my personal post',
			'date_posted' : '5/21/2019'
		}
]

def home(request):
	context = {
				'posts' : posts
	}
	return render(request, 'blog/home.html', context)


def about(request):
	return render(request, 'blog/about.html', { 'title' : 'Yellow About'})
