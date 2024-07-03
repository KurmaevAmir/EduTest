from django.shortcuts import render
from django.views import View
from .models import Profile
# Create your views here.


class HomePageView(View):
    user_authorized = False
    access = 0
    model = Profile
    template_name = 'Main/home.html'

    def get(self, request):
        current_user = request.user
        self.user_authorized = current_user.is_authenticated
        if self.user_authorized:
            self.access = Profile.objects.filter(user=current_user).first().access
        return render(request, self.template_name, {'user_authorized': self.user_authorized,
                                                    'access': self.access})

    def post(self, request):
        pass
