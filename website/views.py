from django.shortcuts import render, get_object_or_404, redirect
from ice_creams.models import *
from website.forms import *
import logging
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s %(levelname)s] %(name)s: %(message)s",)

###


def login_page(req):
    form = GetUserForm()
    message = ""
    user_name = None
    if req.user.is_authenticated:
        user_name = req.user.get_username()
        message = f"{user_name}, you are logged in."
    if "logout" in req.POST:
        logout(req)
        message = f"{user_name} logged out"
        _logger.info(f"{message}")
        user_name = None
    elif "login" in req.POST:
        form = GetUserForm(req.POST)
        if form.is_valid():
            message, user_name = handle_login_form(req, form)
    return render(req, 'login.html', {"form": form, "message": message, "user_name": user_name})


def handle_login_form(req, form):
    user_name = form.cleaned_data['user_name'].capitalize()
    message = ""
    if not User.objects.filter(username=user_name).exists():
        user = User.objects.create_user(username=user_name, password='')
        user.save()
        message = f"New user was created: {user_name}. "
    user = authenticate(username=user_name, password='')
    if user is not None:
        login(req, user)
        message += f"Logged in successfully, {user_name}"
    else:
        message = f"{user_name} login failed"
        user_name = None
    _logger.info(f"{message}")
    return message, user_name


def home(req):
    all_ice_creams = IceCream.objects.all()
    num_ice_creams = IceCream.objects.count()
    return render(req, 'home.html', {"num_ice_creams": num_ice_creams, "all_ice_creams": all_ice_creams})
