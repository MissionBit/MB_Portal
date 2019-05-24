from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def home(request):
	context = {
				'posts' : Post.objects.all()
	}
	return render(request, 'blog/home.html', context)

@login_required
def about(request):
	return render(request, 'blog/about.html', { 'title' : 'Yellow About'})
