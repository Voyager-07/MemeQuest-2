from django import forms

class MemeSearchForm(forms.Form):
    search_query = forms.CharField(max_length=255)
