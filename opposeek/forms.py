from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label="", min_length=1)
