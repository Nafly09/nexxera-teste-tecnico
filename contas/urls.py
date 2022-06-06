from django.urls import path

from contas.views import AccountsView


urlpatterns = [path("accounts/", AccountsView.as_view())]
