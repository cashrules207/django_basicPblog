from urllib.parse import quote_plus
from django.contrib import messages
from django.db.models import Q #https://docs.djangoproject.com/en/1.10/topics/db/queries/ to get this.
								#is an object used to encapsulate a collection of keyword arguments. 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post


def posts_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		# print (form.cleaned_data.get("title"))
		instance.save()
		messages.success(request, "Succesfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def posts_detail(request, id=None):#RETRIEVES AS IN CRUD it also displays individual posts
	instance = get_object_or_404(Post, id=id)
	share_string = quote_plus(instance.content)
	context = {
	"title": instance.title,
	"instance":instance,
	"share_string":share_string,
	}
	return render(request, "post_detail.html", context)

def posts_list(request):#LIST ITEMS FROM THE DATABASE
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	queryset_list = Post.objects.all()
	query = request.GET.get("q") # query is a variable To Get something from the search box....named "q"
	if query: #that is, if it contains something, it should Do THIS-->
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) | #or
			Q(content__icontains=query) | #or
			Q(user__first_name__icontains=query) | #or
			Q(user__last_name__icontains=query)
			).distinct() #so that it will not have duplicate items in there
			
	paginator = Paginator(queryset_list, 10)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list": queryset,
		"title": "all posts from the database"
	}
	
	return render(request, "post_list.html", context)
	#return HttpResponse("<h1>app homepage<h2>")



def posts_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Successfully updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"title": instance.title,
		"instance":instance,
		"form":form,
	}
	return render(request, "post_form.html", context)
	

def posts_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")
	


# Create your views here.
