import django.forms as forms
from googaccount.models import AppCreds

class CredsChoices(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.label

def creds_form(user):
    class CredsForm(forms.Form):
        account = CredsChoices(queryset=AppCreds.objects.filter(user=user), empty_label="")
    return CredsForm    
