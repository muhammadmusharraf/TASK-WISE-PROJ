from django.forms import ModelForm

from app.models import TASKS
class TASKForm(ModelForm):

    class Meta:
        model = TASKS
        fields=['title','status','priority']