"""ice_cream_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import ice_creams.views
import website.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', website.views.home, name="homepage"),
    path('ice-cream/<int:id>', ice_creams.views.info, name="info"),
    path('new_order', ice_creams.views.add_new_order, name="new_order"),
    path('create', ice_creams.views.create_ice_cream, name="create"),
    path('search', ice_creams.views.search_ice_cream, name="search"),
    path('order_history', ice_creams.views.order_history, name="order_history"),
    path('login', website.views.login_page, name="login"),
    path('favorites', ice_creams.views.get_favorites, name="favorites"),
]
