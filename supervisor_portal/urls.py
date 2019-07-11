from django.urls import path
from . import views

urlpatterns = [
	path("", views.render_landing_page),
	path("login", views.log_user_in),
	path("logout", views.logout_user),
	path("create_record", views.create_record),
	path("test", views.test, name="test")
]