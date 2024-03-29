from django import forms
form .models import Mail
class MailFile(forms.ModelForm):
    class Meta:
        model=Mail
        fiels=('file')