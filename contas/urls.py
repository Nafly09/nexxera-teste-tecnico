from django.urls import path

from contas.views import AccountsView, ExtractView


urlpatterns = [
    path("accounts/", AccountsView.as_view()),
    path("accounts/<action>/<account_id>/", AccountsView.as_view()),
    path("extracts/<account_id>/", ExtractView.as_view()),
]
