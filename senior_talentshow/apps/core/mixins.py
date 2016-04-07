from django.http import HttpResponseNotAllowed

from braces.views import JSONResponseMixin


class AjaxFormViewMixin(JSONResponseMixin):

    # since this is an ajax form, we return JSON, not an HttpResponseRedirect, 
    # so the client will never be redirected to the success_url
    success_url = '.'

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            # if request is not AJAX, return 405
            return HttpResponseNotAllowed(['POST'])
        else:
            return super(AjaxFormViewMixin, self).post(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def get_redirect_url(self, *args, **kwargs):
        """
        No need for a redirect URL because we're using AJAX.
        In order to be compatible with Django's FormViews, we'll need
        to define this function.
        """
        return '.'

    def form_valid(self, form):
        # catch the response, so we don't redirect if this is using
        # a Django FormView
        response = super(AjaxFormViewMixin, self).form_valid(form)
        valid_response = self.render_json_response(self.valid_response(form))
        return valid_response

    def form_invalid(self, form):
        invalid_response = self.render_json_response(self.invalid_response(form))
        return invalid_response

    def valid_response(self, form):
        return {'success': True}

    def invalid_response(self, form):
        errors = form.errors
        # include non-field-errors, if any
        errors.update(form.non_field_errors())
        return {'success': False, 'errors': errors}
