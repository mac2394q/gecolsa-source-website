from django import forms
from django.core.validators import MinLengthValidator
from django.urls import reverse
from crispy_forms.helper import FormHelper

from common.models import City
from common.models import Contact
from common.models import Office


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control name',
        })
    )

    mobile_number = forms.CharField(
        label='Celular',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mobile_number',
        })
    )

    comment = forms.CharField(
        label='Mensaje',
        max_length=512,
        validators=[MinLengthValidator(20)],
        widget=forms.Textarea(attrs={
            'placeholder': 'Mensaje...',
            'class': 'form-control comment',
        })
    )

    accept_terms = forms.BooleanField(
        label='Términos y condiciones legales',
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'terms',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_by'].widget = forms.HiddenInput()
        self.fields['contact_by'].required = False
        self.fields['full_path'].widget = forms.HiddenInput()
        self.fields['full_path'].required = False
        self.fields['email'].widget.attrs['class'] = 'form-control email'

    class Meta:
        model = Contact
        fields = (
            'name',
            'mobile_number',
            'email',
            'comment',
            'full_path',
            'contact_by',
        )

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        if len(mobile_number) < 5 or len(mobile_number) > 15:
            self.add_error(
                'mobile_number',
                'Por favor escriba un número de celular válido',
            )

        return mobile_number


class OfficeForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.filter(
            offices__isnull=False
        ).distinct().order_by('title'),
        empty_label="Elige tu sede",
        label='',
    )

    class Meta:
        model = Office
        fields = (
            'city',
        )

    def __init__(self, *args, **kwargs):
        super(OfficeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'get'
        self.helper.form_action = reverse('office_list')
