import datetime

from django.http import Http404, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.utils.timezone import now

from core.mixins import AjaxFormViewMixin
from core.tasks import send_email
from core.utils.general import audition_signup_open
from talentshow.forms import AuditionForm, ChooseAuditionSlotForm, AuditionReminderForm, AuditionSignUpReminderForm
from talentshow.models import Auditioner, AuditionSession, AuditionSignUpReminder


class SetAuditionReminderView(AjaxFormViewMixin, UpdateView):
    form = AuditionReminderForm
    model = Auditioner
    fields = '__all__'

    def valid_response(self, form):
        response = super(SetAuditionReminderView, self).valid_response(form)
        response.update({
            'reminder_text': form.cleaned_data.get('reminder_text'),
            'reminder_email': True,
        })
        return response

    def get_form(self, form_class):
        """
        This is hacky
        """
        data = model_to_dict(self.object)
        data['reminder_text'] = self.request.POST.get('reminder_text')
        return form_class(instance=self.object, data=data)

    def get_object(self):
        secret = self.request.POST.get('secret')
        if not secret:
            raise Http404
        obj = get_object_or_404(Auditioner, secret=secret)
        if not obj.phone:
            raise Http404
        return obj


class AuditionerSignUpView(CreateView):
    model = Auditioner
    form_class = AuditionForm
    template_name = 'talentshow/sign-up.html'

    def post(self, request, *args, **kwargs):
        if not audition_signup_open():
            return HttpResponseNotAllowed(['GET'])
        return super(AuditionerSignUpView, self).post(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(AuditionerSignUpView, self).get_context_data(*args, **kwargs)
        context.update({'audition_signup_open': audition_signup_open()})
        context.update({'audition_signup_reminder_form': AuditionSignUpReminderForm()})
        return context

    def get_success_url(self):
        success_url = reverse('talentshow-choose-slot', kwargs={'secret': self.object.secret})
        return success_url


class ChooseAuditionSlotView(FormView):
    form_class = ChooseAuditionSlotForm
    template_name = 'talentshow/choose-slot.html'


    def get_context_data(self, **kwargs):
        context = super(ChooseAuditionSlotView, self).get_context_data(**kwargs)
        sessions = list(AuditionSession.objects.all())
        for session in sessions:
            if not session.remaining_slots_exist():
                sessions.remove(session)
        sessions.sort(key=lambda x: x.start_time)
        six_hours_ahead = now() + datetime.timedelta(hours=6)
        for session in sessions:
            session.slots = session.auditionslot_set.filter(start_time__gte=six_hours_ahead, auditioner=None).order_by('start_time')
        context['sessions'] = sessions
        return context

    def get(self, request, *args, **kwargs):
        """
        Check the secret, make sure it corresponds to an auditioner who doesn't have a
        slot yet.
        """
        secret = self.kwargs.get('secret')
        if not secret or not Auditioner.objects.filter(secret=secret).exists():
            raise Http404

        if not audition_signup_open():
            return redirect('talentshow-sign-up')

        if Auditioner.objects.filter(secret=secret).exclude(auditionslot=None).exists():
            person = Auditioner.objects.filter(secret=secret).exclude(auditionslot=None)[0]
            reminder_form = AuditionReminderForm(instance=person)
            if not person.phone:
                reminder_form.fields.pop('reminder_text')
            return render(self.request, 'talentshow/sign-up-success.html', {'slot': person.auditionslot, 'auditioner': person, 'reminder_form': reminder_form})

        return super(ChooseAuditionSlotView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Check the secret, make sure it corresponds to an auditioner who doesn't have a
        slot yet.
        """
        secret = self.kwargs.get('secret')
        if not secret or not Auditioner.objects.filter(secret=secret).exists() or not audition_signup_open():
            raise Http404

        if Auditioner.objects.filter(secret=secret).exclude(auditionslot=None).exists():
            person = Auditioner.objects.filter(secret=secret).exclude(auditionslot=None)[0]
            reminder_form = AuditionReminderForm(instance=person)
            if not person.phone:
                reminder_form.fields.pop('reminder_text')
            return render(self.request, 'talentshow/sign-up-success.html', {'slot': person.auditionslot, 'auditioner': person, 'reminder_form': reminder_form})

        return super(ChooseAuditionSlotView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        slot = form.cleaned_data.get('audition_slot')
        secret = self.kwargs.get('secret')
        auditioner = Auditioner.objects.get(secret=secret)
        slot.auditioner = auditioner
        slot.save()

        send_email.delay(
            template_name='audition_confirm',
            subject='Senior Talent Show Audition Confirmation',
            from_email=settings.HARVARD_TALENT_EMAIL,
            recipients=[slot.auditioner.email],
            context={'slot': slot}
        )

        reminder_form = AuditionReminderForm(instance=auditioner)
        if not auditioner.phone:
            reminder_form.fields.pop('reminder_text')

        return render(self.request, 'talentshow/sign-up-success.html', {'slot': slot, 'auditioner': auditioner, 'reminder_form': reminder_form})


class SetAuditionSignUpReminderView(AjaxFormViewMixin, CreateView):
    form = AuditionSignUpReminderForm
    model = AuditionSignUpReminder
