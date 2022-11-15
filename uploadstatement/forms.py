from django import forms    



class AuditDataForm(forms.ModelForm):
    select_file = forms.FileField()


