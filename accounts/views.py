from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, PwdResetConfirmForm, AccountUpdateForm
from django.contrib.auth import get_user_model
from django.urls.base import reverse_lazy
from django.views.generic import View, UpdateView, ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView

User = get_user_model()

class SignUpView(View):
    form_class = RegistrationForm
    template_name = 'accounts/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:user_details', request.user.pk, request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            form = form.save()
            form.save()
            user = authenticate(request, form)
            if user:
                login(request, form)

            return redirect('accounts:user_details', form.username, form.pk)

        else:
            return render(request, self.template_name, {'form': form})

class AccountDetailsView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'user_uuid'
    context_object_name = 'user'
    slug_url_kwarg = 'user_uuid'
    query_pk_and_slug = True
    template_name = 'accounts/user_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.pk == self.get_object().pk:
            context['update_profile_link'] = reverse_lazy('accounts:account_update', self.request.user.user_uuid, self.request.user.pk)
        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AccountUpdateForm
    template_name = "accounts/update_account_form.html"

class PwdResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password/pwd__reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    form_class=PwdResetConfirmForm