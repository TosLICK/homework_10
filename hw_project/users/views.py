from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
# Create your views here.


class SignupView(View):
    template_name = 'users/signup.html'
    form_class = SignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='quotes:root')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, context={"form": self.form_class})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect(to='users:login')
        return render(request, self.template_name, context={"form": form})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotes:root')
