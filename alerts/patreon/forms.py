import django.forms as forms
from patreon.models import PatreonAppCreds

class CredsChoices(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.label

def creds_form(user):
    class CredsForm(forms.Form):
        account = CredsChoices(queryset=PatreonAppCreds.objects.filter(user=user), empty_label="")
    return CredsForm    
