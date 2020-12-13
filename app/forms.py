from django import forms

from app.models import RequestComplaint

from . import data


class ImageForm(forms.Form):
    file = forms.ImageField()


class FileForm(forms.Form):
    file = forms.FileField()


class RequestsComplaintsForm(forms.ModelForm):
    other_relation = forms.CharField(
        max_length=100,
        label='¿Cuál?',
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        type_complaint = cleaned_data.get('type_complaint')
        if type_complaint and int(type_complaint) == int(data.NOT_ANONYMOUS_CHOICE):
            if not cleaned_data.get('full_name'):
                self.add_error('full_name', 'Este campo es obligatorio')

            if not cleaned_data.get('email'):
                self.add_error('email', 'Este campo es obligatorio')

            if not cleaned_data.get('phone_number'):
                self.add_error('phone_number', 'Este campo es obligatorio')

            if not cleaned_data.get('company_relation'):
                self.add_error('company_relation', 'Este campo es obligatorio')

            if (
                cleaned_data.get('company_relation') == data.OTHER_CHOICE and
                not cleaned_data.get('other_relation')
            ):
                self.add_error('other_relation', 'Este campo es obligatorio')

        return cleaned_data

    class Meta:
        model = RequestComplaint
        fields = [
            'full_name',
            'email',
            'phone_number',
            'company_relation',
            'purpose',
            'date',
            'place',
            'acts',
            'document',
            'type_complaint',
        ]
        widgets = {
            'type_complaint': forms.RadioSelect(attrs={'class': 'js-type-complaint'}),
            'company_relation': forms.Select(choices=data.COMPANY_RELATION_CHOICES),
        }
