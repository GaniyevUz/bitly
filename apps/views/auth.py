from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView
from django.shortcuts import render, redirect

from apps.forms import UserForm
from apps.models import User
from apps.utils.token import account_activation_token
from apps.utils.verify_email import send_verification
from root.settings import EMAIL_HOST_USER


class SignUpView(FormView):
    form_class = UserForm
    template_name = 'apps/auth/sign-up.html'
    success_url = reverse_lazy('links_view')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            send_verification(self.request, user)
            return render(self.request, 'apps/parts/temp.html',
                          {'title': 'Account activation', 'context': 'Check your email'})

    def form_invalid(self, form):
        context = {
            'errors': form.errors
        }
        return render(self.request, self.template_name, context)


class SignInView(LoginView):
    template_name = 'apps/auth/sign-in.html'
    next_page = reverse_lazy('links_view')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# class LogOutView(LogoutView):
#     next_page = reverse_lazy('form_view')


def ActivateAccountView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'apps/404.html')
    return redirect('sign_in_view')


def sendmail(request):
    if request.METHOD == 'POST':
        data = request.POST
        User.objects.filter(Q(is_superuser=1) | Q(is_staff=1))
