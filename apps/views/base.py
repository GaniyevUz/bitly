# from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView

from apps.forms import UrlForm
from apps.models import Url, User


class MainFormView(FormView):
    form_class = UrlForm
    template_name = 'apps/index.html'
    # template_name = 'apps/404.html'
    success_url = reverse_lazy('main_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clicked_total = sum(Url.objects.values_list('clicked_count', flat=True))
        users_count = User.objects.count()
        total_links = Url.objects.count()
        context['total_links'] = total_links if total_links > 0 else 0
        context['clicked_total'] = clicked_total if clicked_total > 0 else 0
        context['current_site'] = get_current_site(self.request)
        context['users_count'] = users_count if users_count > 0 else 0
        return context

    def form_valid(self, form):
        url = form.save()
        site = get_current_site(self.request).domain
        if not site.startswith('http'):
            site = 'http://' + site
        url = f'{site}/b/{url.short_name}'
        context = {
            'short_name': url,
        }
        return render(self.request, 'apps/index.html', context)


class LinksView(ListView):
    template_name = 'apps/link-list.html'
    queryset = Url.objects.all()
    context_object_name = 'links'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            if user.is_superuser or user.is_staff:
                query = super().get_queryset()
            return render(request, 'apps/auth/sign-in.html')
        return super().dispatch(request, *args, **kwargs)


class ShortView(View):

    def get(self, request, name, *args, **kwargs):
        url = Url.objects.get(short_name=name)
        # url = get_object_or_404(Url.objects.all(), short_name=name)
        return HttpResponseRedirect(url.long_name)
