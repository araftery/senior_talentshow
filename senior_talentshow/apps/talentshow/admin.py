from django.conf import settings
from django.contrib import admin, messages

from core.tasks import send_email

from talentshow.models import Auditioner, AuditionSlot, AuditionSession, AuditionSignUpReminder


class AuditionerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'description', 'auditionslot', 'reminder_email', 'reminder_text', 'time_registered', 'secret')
    ordering = ('time_registered', 'last_name', 'first_name')


class AuditionSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'session', 'duration', 'location', 'auditioner_full_name')
    ordering = ('start_time',)

    def save_model(self, request, obj, form, change):
        if not change:
            return super(AuditionSlotAdmin, self).save_model(request, obj, form, change)

        send_conf = False
        original_obj = AuditionSlot.objects.get(pk=obj.pk)

        if obj.auditioner != original_obj.auditioner and obj.auditioner is not None:
            send_conf = True

        obj.save()

        if send_conf:
            send_email.delay(
                template_name='audition_confirm',
                subject='Talent Show Audition Confirmation',
                from_email=settings.HARVARD_TALENT_EMAIL,
                recipients=[obj.auditioner.email],
                context={'slot': obj}
            )

            messages.success(request, 'Confirmation email sent.')


class AuditionSignUpReminderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at',)
    ordering = ('created_at',)


admin.site.register(Auditioner, AuditionerAdmin)
admin.site.register(AuditionSlot, AuditionSlotAdmin)
admin.site.register(AuditionSession)
admin.site.register(AuditionSignUpReminder, AuditionSignUpReminderAdmin)
