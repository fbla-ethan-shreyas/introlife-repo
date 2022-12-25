from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from introlife_app.models import Post
from django.views.generic import CreateView

# Create your views here.
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful. ")
            return redirect("home")
        messages.error(request, "Unsuccesful registration. Invalid information")
    form = NewUserForm()
    return render (request = request, template_name = "signup.html", context = {"register_form" : form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request, template_name = "login.html", context = {"login_form" : form})

def logout(request):
    auth_logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

def platform(request):
    post = Post.objects.all()
    return render(request, "platform.html", {"post" : post})

class CreatePostView(CreateView):
    model = Post
    template_name = "createpost.html"
    fields = ('title', 'body')

    #passes current user to author field
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)