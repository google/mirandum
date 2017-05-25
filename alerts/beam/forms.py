import django.forms as forms
from beam.models import BeamAppCreds

class CredsChoices(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.label

def creds_form(user):
    class CredsForm(forms.Form):
        account = CredsChoices(queryset=BeamAppCreds.objects.filter(user=user), empty_label="")
    return CredsForm    
