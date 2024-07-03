from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Profile
# Create your views here.


class HomePageView(TemplateView):
    template_name = 'Main/home.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_authorized = request.user.is_authenticated
        if self.user_authorized:
            self.profile = get_object_or_404(Profile, user=request.user)
        else:
            self.profile = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_authorized'] = self.user_authorized
        context['access'] = self.profile.access if self.profile else 0
        return context

    def post(self, request):
        pass
