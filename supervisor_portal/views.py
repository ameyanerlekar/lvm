from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RecordForm

def render_landing_page(request):
	if request.user.is_authenticated:
		return render_userpage(request)
	else:
		return render(request, "landing.html")

	
def log_user_in(request):
	if request.method == "POST" and not request.user == "AnonymousUser":	
		user = authenticate(request, username = request.POST.get("username"), password = request.POST.get("password"))
		if user is not None:
			login(request, user)
			return render_userpage(request)
		else:
			return render(request, "landing.html", {"message": "Incorrect Username or Password!"})
	elif request.user.is_authenticated:
		user = User.objects.get(username = request.user)
		return render_userpage(request)
	
	
def render_userpage(request):
	if request.user.is_authenticated:
		user = User.objects.get(username = request.user)
		user_groups = [ group["name"] for group in user.groups.all().values() ]
		if "management" in user_groups:
			form = RecordForm()
			return render(request, "userpage.html", {"user": user, "record_form": form})
		else:
			return render(request, "userpage.html", {"user": user})
	
	
def logout_user(request):
	if request.user.is_authenticated and request.method == "POST":
		logout(request)
		return render_landing_page(request)
	
	
def test(request):
	user = User.objects.get(username = "amrutanerlekar")
	print(user.groups.all().values()[0]["name"])
	return HttpResponse("check the console")
	
	
	