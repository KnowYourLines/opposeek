from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label="Search", min_length=1)
