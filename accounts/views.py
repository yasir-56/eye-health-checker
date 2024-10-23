from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from .models import CustomUser
from .forms import CustomUserSignupForm, CustomUserLoginForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy



class index(View):
    def get(self, request):
        return render(request, "accounts/index.html")




class Login(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        form = CustomUserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserLoginForm(request.POST, request=request)

        if form.is_valid():
            # Authenticate the user and log them in
            user = form.get_user()
            login(request, user)
            print("User logged in successfully!")  # Debugging statement

            # Redirect to profile (or any other target page)
            return redirect('dashboard')
        else:
            # If the form is not valid, re-render the page with form errors
            print("Login failed: Invalid username or password")  # Debugging statement
            return render(request, self.template_name, {'form': form})




class CustomLogoutView(LogoutView):
   
    next_page = reverse_lazy('index')  




class SignupView(CreateView):
    model = CustomUser
    form_class = CustomUserSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful signup

    def form_valid(self, form):
        # Save the new user without logging them in
        form.save()
        return super().form_valid(form)





class DashboardView(View):
    def get(self, request):
        return render(request, 'accounts/dashboard.html')

