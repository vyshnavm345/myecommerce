from django import forms


class DateRangeForm(forms.Form):
    start_month = forms.DateField(widget=forms.SelectDateWidget(years=range(2022, 2030)))
    end_month = forms.DateField(widget=forms.SelectDateWidget(years=range(2022, 2030)))