from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from apps.views import MainFormView, ShortView, LinksView, SignUpView, SignInView, sendmail, ActivateAccountView

urlpatterns = [
    path('', MainFormView.as_view(), name='form_view'),
    path('links', LinksView.as_view(), name='links_view'),
    path('links/page/<int:page>', LinksView.as_view(), name='links_view'),

    path('sign-up', SignUpView.as_view(), name='sign_up_view'),
    path('activate_account/<str:uidb64>/<str:token>', ActivateAccountView, name='activate_user'),
    path('send-mail', sendmail, name='send_mail_view'),
    path('sign-in', SignInView.as_view(), name='sign_in_view'),

    path('logout', LogoutView.as_view(next_page=reverse_lazy('form_view')), name='log_out_view'),
    path('forgot-password', LinksView.as_view(), name='forgot_password_view'),
    path('change-password', LinksView.as_view(), name='change_password_view'),
    path('b/<str:name>', ShortView.as_view(), name='short_view'),
]

