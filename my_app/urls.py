from django.urls import path
from . import views


urlpatterns = [
  path("", views.home, name="home"),
  path("login/", views.login_user, name="login"),
  path("sign_up/", views.sign_up, name="sign_up"),
  path("set_paid/<int:pk>/", views.set_paid, name="set_paid"),
  path("pojistenec/<int:pk>/pridat_pojisteni", views.pridat_pojisteni, name="pridat_pojisteni"),
  path("detail_pojistence/<int:pk>/", views.detail_pojistence, name="detail_pojistence"),
  path("odebrat_pojisteni_pojistenci/<int:pk>/<int:id>", views.odebrat_pojisteni_pojistenci, name="odebrat_pojisteni_pojistenci"),

  # CRUD POJISTENEC
  path("vytvorit_pojistence", views.vytvorit_pojistence, name="vytvorit_pojistence"),
  path("pojistenci/", views.pojistenci, name="pojistenci"),
  path("pojistenec/<int:pk>/upravit", views.upravit_pojistence, name="upravit_pojistence"),
  path("pojistenec/<int:pk>/smazat", views.odstranit_pojistence, name="odstranit_pojistence"),

  # CRUD POJISTENI
  path("pojisteni/", views.pojisteni, name="pojisteni"),
  path("vytvorit_pojisteni/", views.vytvorit_pojisteni, name="vytvorit_pojisteni"),
  path("pojisteni/<int:pk>/odstranit", views.odstranit_pojisteni, name="odstranit_pojisteni"),

  # POJISTNA UDALOST
  path("pojistna-udalost/", views.pojistna_udalost, name="pojistna_udalost"),
]