from django.db import models
import datetime

# Create your models here.
class Ticket(models.Model):
	STATUS_CHOICES = (
		("PENDING", "PENDING"),
		("RESOLVED", "RESOLVED")
	)
	raised_by = models.CharField(max_length = 30)
	body = models.TextField()
	status = models.CharField(max_length = 1, choices = STATUS_CHOICES, default = "PENDING")
	date_of_raising = models.DateTimeField(auto_now = True)
	date_of_resolving = models.DateTimeField(null = True)
	
	def mark_resolved(self):
		if self.status == "PENDING":
			self.status = "RESOLVED"
			self.date_of_resolving = datetime.datetime.now()
			self.save()
			return "Ticket (" + self.id + ") has been marked as resolved."
		else:
			raise Exception("This Ticket (" + self.id + ") was already resolved.")
			
			
class Record(models.Model):
	for_floor = models.IntegerField()
	for_room = models.CharField(max_length=10)
	body = models.TextField()
	date = models.DateField(auto_now = True)
	