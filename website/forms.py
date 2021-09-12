from django import forms


class GetUserForm(forms.Form):
    user_name = forms.CharField(max_length=20)
