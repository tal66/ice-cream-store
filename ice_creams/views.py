from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from ice_creams.models import *
from ice_creams.forms import *
from django.http import HttpRequest
from django.db import transaction
from django.contrib.auth.decorators import login_required
import logging

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s %(levelname)s] %(name)s: %(message)s",)


def info(req, id):
    message = ""
    ice_cream = get_object_or_404(IceCream, pk=id)
    if "add_favorite" in req.POST:
        user = req.user
        user_name = user.get_username()
        if user_name is None:
            message = "Please login first"
        else:
            add_to_favorites(user, ice_cream)
            message = "saved to favorites"
    return render(req, 'info.html', {"ice_cream": ice_cream, "message": message})


##

@login_required
def add_new_order(req):
    user_name = req.user.get_username()
    message = ""
    if req.method == 'GET':
        get_num_form = GetNumItemsForm()
        return render(req, 'order.html', {"get_num_form": get_num_form})
    elif "get_num_items" in req.POST:
        num_items = _get_num_items(req)
        _logger.info(
            f"Order Process: User {user_name} is ordering {num_items} types.")
        formset = forms.formset_factory(BuyIceCreamForm, extra=num_items)
    elif "get_order" in req.POST:
        formset, message = _handle_order(req)
    return render(req, 'order.html', {"formset": formset, "message": message, "user_name": user_name})


def _handle_order(req):
    BuyIceCreamFormSet = forms.formset_factory(
        BuyIceCreamForm, extra=req.POST['form-TOTAL_FORMS'])
    formset = BuyIceCreamFormSet(req.POST)
    user_name = req.user.get_username()

    with transaction.atomic():
        if formset.is_valid():
            message_list = ['thanks. your order was saved.']
            order = Order(user=req.user)
            order.save()
            for f in formset:
                item_message = _create_order_item(f, order)
                message_list.append(item_message)
            message_list.append(f"\nTotal: ${order.get_total_price()}")
            message = ''.join(message_list)
            _logger.info(
                f"Order Process: User {user_name} ordered: {''.join(message_list[1:])}.")
        else:
            message = 'invalid'
    return formset, message


def _create_order_item(form, order):
    ice_cream = form.cleaned_data['ice_cream']
    q = form.cleaned_data['quantity']
    p = ice_cream.price_usd
    orderitem = OrderItem(item=ice_cream, quantity=q,
                          order=order, unit_price_usd=p)
    orderitem.save()
    message = f"\n{str(orderitem.quantity)} x  {str(orderitem.item)}"
    return message


def _get_num_items(req):
    form = GetNumItemsForm()
    if req.method == 'POST':
        form = GetNumItemsForm(req.POST)
        if form.is_valid():
            return form.cleaned_data['num_items']


@ login_required
def order_history(req):
    user = req.user
    all_orders = Order.objects.filter(user=user)
    form = SelectOrderForm(all_orders=all_orders)

    if "delete_order" in req.POST:
        delete_order(SelectOrderForm(req.POST, all_orders=all_orders), user)

    order_dict = {}
    for order in all_orders:
        order_dict[order] = order.orderitem_set.all()

    return render(req, 'order_history.html', {"order_dict": order_dict, "user_name": user.get_username(), 'form': form})


def delete_order(form, user):
    if form.is_valid():
        order = form.cleaned_data['order']
        _logger.info(
            f"{user} is Deleting \"{order}\" made by {order.user}.")
        order.delete()


##

def search_ice_cream(req):
    result = None
    form = SearchIceCreamForm()
    if req.method == 'POST':
        form = SearchIceCreamForm(req.POST)
        if form.is_valid():
            search_input = form.cleaned_data['user_search']
            result = get_search_results(req, search_input)
    return render(req, 'search.html', {'form': form, "result": result})


def get_search_results(req, search_input):
    if "search_by_name" in req.POST:
        result = IceCream.objects.filter(
            name__icontains=search_input).order_by('name')
    else:
        result = IceCream.objects.filter(
            description__icontains=search_input).order_by('name')
    return result


##

def create_ice_cream(req):
    form = CreateIceCreamForm()
    message = ""
    if req.method == 'POST':
        form = CreateIceCreamForm(req.POST)
        if form.is_valid():
            form.save()
            message = 'thanks. your ice cream was added'
        else:
            message = 'invalid'
    return render(req, 'create.html', {"form": form, "message": message})


##

@ login_required
def get_favorites(req):
    user = req.user
    user_name = user.get_username()
    try:
        user_favorites = UserProfile.objects.get(user=user).favorites.all()
    except:
        user_favorites = []
    return render(req, 'favorites.html', {"user_favorites": user_favorites, "user_name": user_name})


def add_to_favorites(user, ice_cream):
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    userprofile.favorites.add(ice_cream)
    userprofile.save()
