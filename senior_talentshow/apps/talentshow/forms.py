from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from crispy_forms.layout import HTML
from crispy_forms.layout import Field, Hidden
from crispy_forms.layout import Fieldset
from crispy_forms.layout import Layout
from crispy_forms.layout import MultiField
from crispy_forms.layout import Submit, Button
from crispy_forms.bootstrap import StrictButton

from talentshow.models import Auditioner, AuditionSlot


class ChooseAuditionSlotForm(forms.Form):
    audition_slot = forms.ModelChoiceField(queryset=AuditionSlot.objects.filter(auditioner=None).order_by('start_time'), widget=forms.RadioSelect)

def __init__(self, *args, **kwargs):
        super(ChooseAuditionSlotForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.form_id = 'audition-slot-form'
        self.helper.form_name = 'audition-slot-form'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True


class AuditionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AuditionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.form_id = 'audition-form'
        self.helper.form_name = 'audition-form'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True

        self.fields['description'].label = '(Very) brief description of act'
        self.fields['props_info'].label = 'Props and A/V Needs (leave blank if none)'

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class="form-control"),
                    css_class="form-group"
                ),
                Div(
                    Field('last_name', css_class="form-control"),
                    css_class="form-group"
                ),
                css_class="col-md-6"
            ),
            Div(
                Div(
                    Field('email', css_class="form-control"),
                    css_class="form-group"
                ),
                Div(
                    Field('phone', css_class="form-control"),
                    css_class="form-group"
                ),
                css_class="col-md-6"
            ),
            Div(
                Div(
                    Field('description', css_class="form-control"),
                    css_class="form-group"
                ),
                css_class="col-md-12"
            ),
            Div(
                Div(
                    Field('props_info', css_class="form-control"),
                    css_class="form-group"
                ),
                css_class="col-md-12"
            ),
            Div(
                Submit('submit', 'Submit', css_class="btn bg-red block"),
            ),
            Div(
                Div(
                    HTML("{% load talentshow_tags %}Groups of up to 4 are permitted. Only one member of a group needs to sign up for an audition. Act should be performance-ready. On the next page, you'll be asked to pick a time slot for your audition. If you have any questions, or to change an existing audition time, please email us at {% talentshow_email %}."),
                    css_class="col-sm-12 help-text",
                ),
            ),
        )

    class Meta:
        model = Auditioner
        fields = ('first_name', 'last_name', 'email', 'phone', 'description', 'props_info')


class AuditionReminderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AuditionReminderForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.form_id = 'audition-reminder-form'
        self.helper.form_name = 'audition-reminder-form'
        self.helper.label_class = 'control-label'
        self.fields['reminder_text'].label = 'Send me a reminder text an hour before my audition.'

        self.helper.layout = Layout(
            Div(
                Field('reminder_text', wrapper_class="checkbox"),
                Field('secret', type="hidden"),
                StrictButton('Save', css_class="btn btn-primary bg-red js-reminder-submit"),
            ),
        )

    class Meta:
        model = Auditioner
        fields = ('reminder_text', 'secret')


class AuditionSignUpReminderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AuditionSignUpReminderForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = ''
        self.helper.form_id = 'audition-signup-reminder-form'
        self.helper.form_name = 'audition-signup-reminder-form'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Div(
                Div(
                    Field('first_name', css_class="form-control"),
                    css_class="form-group"
                ),
                css_class="col-md-6"
            ),
            Div(
                Div(
                    Field('last_name', css_class="form-control"),
                    css_class="form-group"
                ),
                css_class="col-md-6"
            ),
            Div(
                Div(
                    Field('email', css_class="form-control"),
                    css_class="form-group"
                ),
                css_class="col-md-12"
            ),
            Div(
                Submit('submit', 'Set Reminder', css_class="btn bg-red block js-signup-reminder-btn"),
            ),
        )

    class Meta:
        model = Auditioner
        fields = ('first_name', 'last_name', 'email',)
