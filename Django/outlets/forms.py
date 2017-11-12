from django import forms

from .models import Outlet


class OutletCreateForm(forms.ModelForm):

    class Meta:
        model = Outlet
        fields = ['name', 'address', 'category']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == "check validation":
            raise forms.ValidationError('Not a valid name')
        return name

# class OutletCreateForm(forms.Form):
#     name = forms.CharField()
#     address = forms.CharField(required=False)
#     category = forms.CharField(required=False)

#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if name == 'Check':
#             raise forms.ValidationError('Not a valid name')
#         return name
