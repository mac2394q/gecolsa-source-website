from django import forms
from django.contrib.sites.models import Site

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import HTML
from constance import config

from cms.models import Communication
from cms.models import CommunicationCategory
from cms.models import SatelliteMonitoringContact
from cms.models import Page


def append_children_choices(page, parent_choices, prefix):
    prefix += '-'
    for child_page in page.children.all():
        parent_choices.append(
            (child_page.id, '{0} {1}'.format(prefix, child_page.title))
        )
        append_children_choices(child_page, parent_choices, prefix)


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = (
            'title',
            'summary',
            'image',
            'parent',
            'position',
            'content',
            'has_children_accordion',
            'show_children',
            'meta_title',
            'meta_description',
        )

    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop('object', None)
        super().__init__(*args, **kwargs)
        if not self.object and 'parent' in self.fields:
            parent_choices = [('', '---------')]

            for page in self.fields['parent'].queryset.filter(parent=None):
                parent_choices.append((page.id, page.title))
                append_children_choices(page, parent_choices, '')
            self.fields['parent'].choices = parent_choices

    def clean(self):
        cleaned_data = super(PageForm, self).clean()
        parent = cleaned_data.get('parent')
        image = cleaned_data.get('image')
        has_children_accordion = cleaned_data.get('has_children_accordion')
        footer_title_1 = cleaned_data.get('footer_title_1')
        footer_link_1 = cleaned_data.get('footer_link_1')
        footer_image_1 = cleaned_data.get('footer_image_1')
        footer_title_2 = cleaned_data.get('footer_title_2')
        footer_link_2 = cleaned_data.get('footer_link_2')
        footer_image_2 = cleaned_data.get('footer_image_2')
        footer_title_3 = cleaned_data.get('footer_title_3')
        footer_link_3 = cleaned_data.get('footer_link_3')
        footer_image_3 = cleaned_data.get('footer_image_3')

        if not self.object and not parent:
            msg = 'No se puede crear páginas del primer nivel.'
            self.add_error('parent', msg)

        if self.object and self.object.parent is not None and parent is None:
            msg = 'No se puede crear páginas del primer nivel.'
            self.add_error('parent', msg)

        if not parent and has_children_accordion:
            msg = 'No se puede mostrar el acordeon si no tiene página padre.'
            self.add_error('has_children_accordion', msg)

        if parent and parent.parent:
            if (
                parent.has_children_accordion and
                not has_children_accordion
            ):
                msg = '''Debe seleccionar mostrar el menú lateral al igual que
                la página padre'''
                self.add_error('has_children_accordion', msg)
            elif (
                not parent.has_children_accordion and
                has_children_accordion
            ):
                msg = '''No puede seleccionar mostrar el menú lateral al igual
                que la página padre'''
                self.add_error('has_children_accordion', msg)

        if not image and not parent:
            msg = 'La página del primer nivel debe tener una imagen.'
            self.add_error('image', msg)

        if (
            footer_title_1 or footer_link_1 or footer_image_1 or
            footer_title_2 or footer_link_2 or footer_image_2 or
            footer_title_3 or footer_link_3 or footer_image_3
        ) and not (
            footer_title_1 and footer_link_1 and footer_image_1 and
            footer_title_2 and footer_link_2 and footer_image_2 and
            footer_title_3 and footer_link_3 and footer_image_3
        ):
            msg = '''Tiene que completar todos los campos \
                  de los bloques inferiores de la página.'''
            self.add_error(None, msg)


class CommunicationForm(forms.ModelForm):

    class Meta:
        model = Communication
        fields = (
            'title',
            'category',
            'image',
            'content',
            'extended_content',
            'event_date',
            'event_hour',
            'event_place',
            'meta_title',
            'meta_description',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super(CommunicationForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = \
            self.fields['category'].queryset.exclude(slug='eventos')

    def clean(self):
        cleaned_data = super(CommunicationForm, self).clean()
        footer_title_1 = cleaned_data.get('footer_title_1')
        footer_link_1 = cleaned_data.get('footer_link_1')
        footer_image_1 = cleaned_data.get('footer_image_1')
        footer_title_2 = cleaned_data.get('footer_title_2')
        footer_link_2 = cleaned_data.get('footer_link_2')
        footer_image_2 = cleaned_data.get('footer_image_2')
        footer_title_3 = cleaned_data.get('footer_title_3')
        footer_link_3 = cleaned_data.get('footer_link_3')
        footer_image_3 = cleaned_data.get('footer_image_3')

        if (
            footer_title_1 or footer_link_1 or footer_image_1 or
            footer_title_2 or footer_link_2 or footer_image_2 or
            footer_title_3 or footer_link_3 or footer_image_3
        ) and not (
            footer_title_1 and footer_link_1 and footer_image_1 and
            footer_title_2 and footer_link_2 and footer_image_2 and
            footer_title_3 and footer_link_3 and footer_image_3
        ):
            msg = 'Tiene que completar todos los campos ' \
                  'de los bloques inferiores de la página.'
            self.add_error(None, msg)


class EventForm(forms.ModelForm):

    class Meta:
        model = Communication
        fields = (
            'title',
            'category',
            'image',
            'content',
            'extended_content',
            'event_date',
            'event_hour',
            'event_place',
            'meta_title',
            'meta_description',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event_date'].required = True
        self.fields['event_hour'].required = True
        self.fields['event_city'].required = True

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        footer_title_1 = cleaned_data.get('footer_title_1')
        footer_link_1 = cleaned_data.get('footer_link_1')
        footer_image_1 = cleaned_data.get('footer_image_1')
        footer_title_2 = cleaned_data.get('footer_title_2')
        footer_link_2 = cleaned_data.get('footer_link_2')
        footer_image_2 = cleaned_data.get('footer_image_2')
        footer_title_3 = cleaned_data.get('footer_title_3')
        footer_link_3 = cleaned_data.get('footer_link_3')
        footer_image_3 = cleaned_data.get('footer_image_3')

        if (
            footer_title_1 or footer_link_1 or footer_image_1 or
            footer_title_2 or footer_link_2 or footer_image_2 or
            footer_title_3 or footer_link_3 or footer_image_3
        ) and not (
            footer_title_1 and footer_link_1 and footer_image_1 and
            footer_title_2 and footer_link_2 and footer_image_2 and
            footer_title_3 and footer_link_3 and footer_image_3
        ):
            msg = 'Tiene que completar todos los campos ' \
                  'de los bloques inferiores de la página.'
            self.add_error(None, msg)


class CommunicationCategoryForm(forms.ModelForm):

    class Meta:
        model = CommunicationCategory
        fields = (
            'title',
            'position',
            'footer_title_1',
            'footer_link_1',
            'footer_image_1',
            'footer_title_2',
            'footer_link_2',
            'footer_image_2',
            'footer_title_3',
            'footer_link_3',
            'footer_image_3',
        )

    def clean(self):
        cleaned_data = super(CommunicationCategoryForm, self).clean()
        footer_title_1 = cleaned_data.get('footer_title_1')
        footer_link_1 = cleaned_data.get('footer_link_1')
        footer_image_1 = cleaned_data.get('footer_image_1')
        footer_title_2 = cleaned_data.get('footer_title_2')
        footer_link_2 = cleaned_data.get('footer_link_2')
        footer_image_2 = cleaned_data.get('footer_image_2')
        footer_title_3 = cleaned_data.get('footer_title_3')
        footer_link_3 = cleaned_data.get('footer_link_3')
        footer_image_3 = cleaned_data.get('footer_image_3')

        if (
            footer_title_1 or footer_link_1 or footer_image_1 or
            footer_title_2 or footer_link_2 or footer_image_2 or
            footer_title_3 or footer_link_3 or footer_image_3
        ) and not (
            footer_title_1 and footer_link_1 and footer_image_1 and
            footer_title_2 and footer_link_2 and footer_image_2 and
            footer_title_3 and footer_link_3 and footer_image_3
        ):
            msg = 'Tiene que completar todos los campos ' \
                  'de los bloques inferiores de la página.'
            self.add_error(None, msg)


class SatelliteMonitoringContactForm(forms.ModelForm):

    class Meta:
        model = SatelliteMonitoringContact

        fields = (
            'name',
            'company',
            'email',
            'phone',
            'address',
            'machine',
        )

    def __init__(self, *args, **kwargs):
        super(SatelliteMonitoringContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        site = Site.objects.get_current()
        self.helper.layout = Layout(
            'name',
            'company',
            'email',
            'phone',
            'address',
            'machine',
            HTML('''
                <p>El titular de la información que diligencie el formulario de
                nuestro link "Registrarse" o "VISIONLINK",
                manifiesta en forma libre y expresa que los datos personales e
                información suministrada, está aceptando y autorizando
                a {0} para que incluya esta información en su base de
                datos y pueda hacer uso de la misma para efectos de estudios
                de mercados, publicidad, compartir con fábrica o cualquier
                otro tipo de uso comercial propio de la Compañia, bajo
                la normatividad vigente y la <a href="/maquinaria/legal/">
                política de Tratamiento de la Información y Datos Personales
                de {0}</a>. El Titular de la información podrá en cualquier
                momento aclarar, completar, rectificar o solicitar la
                eliminación de esta información, contactándose al correo
                electrónico: <a href="mailto:{1}">{1}</a>. Los términos y
                condiciones establecidos en la aplicación de VisionLink, deben
                ser revisados por el cliente y/o titular de la información en
                la pagina web:
                <a href="https://www.myvisionlink.com">www.myvisionlink.com</a>
                ya que no son responsabilidad de {0} sino directamente de
                VISIONLINK como proveedor de la aplicación, bajo los términos
                allí señalados.</p>
            '''.format(
                site.name,
                config.EMAIL_GECOLSA_LEGAL
            )),
            'accept_terms',
        )
