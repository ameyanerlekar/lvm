from django.forms import ModelForm
from .models import Record, Ticket

class RecordForm(ModelForm):
	class Meta:
		model = Record
		fields = ["for_floor", "for_room", "body"]