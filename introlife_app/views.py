from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from introlife_app.models import Post
from django.views.generic import CreateView, DetailView
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

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
    paginator = Paginator(post, 1)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "platform.html", {"post" : post, "page_obj" : page_obj})

class CreatePostView(CreateView):
    model = Post
    template_name = "createpost.html"
    fields = ('title', 'body')

    #passes current user to author field
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = "post.html"

def subscribe(email):
    mailchimp = Client()
    mailchimp.set_config({
        "api_key" : api_key,
        "server" : server,
    })
    
    member_info = {
        "email_address" : email,
        "status" : "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occured: {}".format(error.text))

def subscription(request):
    if request.method == "POST":
        email = request.POST['email']
        subscribe(email)
        messages.success(request, "Your email has been received. Thank you!")

    return render(request, "subscribe.html")