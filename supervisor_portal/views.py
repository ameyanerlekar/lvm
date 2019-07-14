from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RecordForm
from .models import Record
import datetime

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
	
	
def render_userpage(request, message=None):
	if request.user.is_authenticated:
		user = User.objects.get(username = request.user)
		user_groups = [ group["name"] for group in user.groups.all().values() ]
		if "management" in user_groups:
			form = RecordForm()
			return render(request, "userpage.html", {"user": user, "record_form": form, "message": message})
		elif "trustee" in user_groups:
			try:
				records = Record.objects.all()[-1:-10]
			except Exception as e:
				records = Record.objects.all()
			#if len(records) == 0:
			#	message = "-- No Records To Show Yet --"
			return render(request, "userpage.html", {"records": records, "message": message})
		else:
			return render(request, "userpage.html", {"user": use, "message": message})
	
	
def logout_user(request):
	if request.user.is_authenticated and request.method == "POST":
		logout(request)
		return render_landing_page(request)
	
	
def create_record(request):
	floor = request.POST.get("for_floor")
	room = request.POST.get("for_room")
	body = request.POST.get("body")
	Record.objects.create(
		for_floor = floor,
		for_room = room,
		body = body
	)
	return redirect("/supervisor_portal/")
	
	
def modify_record(request):
	if request.user.is_authenticated:
		action = request.POST.get("action")
		record_id = request.POST.get("record_id")
		if action == "edit":
			record_to_edit = Record.objects.get(id = record_id)
			form = RecordForm()
			return render(request, "userpage.html", {"record_to_edit": record_to_edit})
		else:
			record_to_delete = Record.objects.get(id = record_id)
			record_to_delete.delete()
			return render_userpage(request, "Record Deleted Successfully!")
		
		
def edit_record(request):
	if request.user.is_authenticated:
		record_to_edit = Record.objects.get(id = request.POST.get("record_to_edit_id"))
		record_to_edit.for_floor = request.POST.get("for_floor")
		record_to_edit.for_room = request.POST.get("for_room")
		record_to_edit.body = request.POST.get("body")
		record_to_edit.save()
		return render_userpage(request, "Record Edited Successfully!")
	
	
def test(request):
	record = Record.objects.all()
	print(record)
	return HttpResponse("check the console")
	
	
	