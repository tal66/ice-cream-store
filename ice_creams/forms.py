from django import forms
from ice_creams.models import *
from django.core.validators import MinValueValidator, MaxValueValidator


class SelectOrderForm(forms.Form):
    class Meta:
        model = Order

    def __init__(self, *args, **kwargs):
        all_orders = kwargs.pop('all_orders', None)
        super(SelectOrderForm, self).__init__(*args, **kwargs)
        self.fields['order'] = forms.ModelChoiceField(
            queryset=all_orders, empty_label=None)


class SearchIceCreamForm(forms.Form):
    user_search = forms.CharField(label='Search', max_length=20)


CreateIceCreamForm = forms.modelform_factory(
    IceCream,
    fields=["name", "description", "ingredients"]
)


class GetNumItemsForm(forms.Form):
    num_items = forms.IntegerField(
        label='Number of flavors', min_value=1, max_value=10)


class BuyIceCreamForm(forms.Form):
    ice_cream = forms.ModelChoiceField(
        queryset=IceCream.objects, empty_label=None,)
    quantity = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
