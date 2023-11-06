from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label="", min_length=1)
    is_recent_trend = forms.BooleanField(
        required=False, label="Is new trend? (may take longer)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
