from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import Pojistenec, Pojisteni
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings


# home view
def home(request):
  return render(request, "home.html")


# přihlášení view
def login_user(request):
  hlaska = ""
  # získáme uživatelské jméno a heslo
  if request.method == "POST":
    username = request.POST.get("username")
    password1 = request.POST.get("password1")

    user = authenticate(request, username=username, password=password1)

    # pokud uživatel existuje, tak ho přesměrujeme... 
    if user is not None:
      login(request, user)
      return redirect("pojistenci")
    else:
      # v opačném případě se bude muset registrovat... 
      hlaska = "Uživatelské jméno nebo heslo není správné."

  return render (request, 'registration/login.html', {"hlaska": hlaska})


# registrace view
def sign_up(request):
  hlaska = ""
  cisla = [1,2,3,4,5,6,7,8,9,0]
  if request.method == "POST":
    uname = request.POST.get("username")
    email = request.POST.get("email")
    pass1 = request.POST.get("password1")
    pass2 = request.POST.get("password2")

    if User.objects.filter(username=uname).exists():
      hlaska = f'Uživatel "{uname}" již existuje.'

    elif User.objects.filter(email=email).exists():
      hlaska = f'Emailová adresa "{email}" již existuje.'

    elif pass1 != pass2:
      hlaska = "Hesla se neshodují."

    # kontrola délky hesla
    elif len(pass1) < 8:
      hlaska = "Heslo musí být alespoň 8 znaků dlouhé."

    # kontrola alespon jednoho čísla v hesle
    elif not any(char.isdigit() for char in pass1):
      hlaska = "Heslo musí obsahovat alespoň jednu číslici."
    
    else:
      my_user = User.objects.create_user(uname, email, pass1)
      my_user.save()
      send_mail(message=f'Ahoj uživateli "{my_user}", tvůj účet v mé aplikaci byl úsplěšně zaregistrován.', 
              subject="Vítejte v mé aplikaci", 
              from_email=settings.EMAIL_HOST_USER, recipient_list=[f"{email}"], 
              fail_silently= False)
      messages.success(request, f"Nový uživatel {uname} byl úspěšně zaregistrován a byl mu odeslán uvítací email.")
      return redirect("login")


  return render(request, "registration/sign_up.html", {"hlaska": hlaska})


# detail pojištěnce

def detail_pojistence(request, pk):
  pojistenec = Pojistenec.objects.get(id=pk)

  return render(request, "detail_pojistence.html", {"pojistenec": pojistenec})

# odebrat pojištění pojištěnci

def odebrat_pojisteni_pojistenci(request, pk, id):
  pojistenec = Pojistenec.objects.get(id=pk)
  pojisteni = Pojisteni.objects.get(id=id)

  if request.method == "POST":
    pass
    vyber_pojisteni = Pojisteni.objects.get(id=id)
    pojistenec.pojisteni.remove(vyber_pojisteni)
    return redirect("pojistenci")

  return render(request, "odebrat_pojisteni_pojistenci.html", {"pojistenec": pojistenec, "pojisteni": pojisteni})


#####
# CRUD POJISTENEC
#####

# vytvoření view 
def vytvorit_pojistence(request):
  if request.method == "POST":
    name = request.POST['name']
    surname = request.POST['surname']
    email = request.POST['email']
    phone = request.POST['phone']
    street = request.POST['street']
    city = request.POST['city']
    psc = request.POST['psc']
    novy_pojistenec = Pojistenec(name=name, surname=surname, email=email, phone=phone, street=street, city=city, psc=psc)
    
    novy_pojistenec.author = request.user 
    novy_pojistenec.save()

    messages.success(request, "Nový pojištěnec byl úspěšně vytvořen.")
    return redirect("pojistenci")
  return render(request, "vytvorit_pojistence.html")

# pojistenci view, který vidí jen přihlášený uživatel
@login_required(login_url= "/login")
def pojistenci(request):
  pocet_pojistencu = Pojistenec.objects.count()
  pojistenci = Pojistenec.objects.all().order_by('-id')


  # pagination = stránkování
  paginator = Paginator(pojistenci, 4)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  return render(request, "pojistenci.html", {"pojistenci": pojistenci, "pocet_pojistencu": pocet_pojistencu, "page_obj": page_obj})

# úprava view

def upravit_pojistence(request,pk):
  pojistenec = Pojistenec.objects.get(id=pk)
  if request.method == "POST":

    Pojistenec.objects.filter(id=pk).update(name=request.POST['name'])
    Pojistenec.objects.filter(id=pk).update(surname=request.POST['surname'])
    Pojistenec.objects.filter(id=pk).update(email=request.POST['email'])
    Pojistenec.objects.filter(id=pk).update(phone=request.POST['phone'])
    Pojistenec.objects.filter(id=pk).update(street=request.POST['street'])
    Pojistenec.objects.filter(id=pk).update(city=request.POST['city'])
    Pojistenec.objects.filter(id=pk).update(psc=request.POST['psc'])

    return redirect("pojistenci")

  return render(request, "upravit_pojistence.html", {"pojistenec": pojistenec})


# smazání view
def odstranit_pojistence(request, pk):
  pojistenec = Pojistenec.objects.get(id=pk)
  if request.method == "POST":
    pojistenec.delete()
    return redirect("pojistenci")
  return render(request, "odstranit_pojistence.html", {"pojistenec": pojistenec})

# přidat pojištění view
def pridat_pojisteni(request, pk):
  pojistenec = Pojistenec.objects.get(id=pk)
  vsechna_pojisteni = Pojisteni.objects.all()
  if request.method == "POST":
    pojisteni = request.POST.getlist("pojisteni_list")
    for vyber_pojisteni in pojisteni:
      if Pojisteni.objects.filter(id=vyber_pojisteni):
        vyber_pojisteni = Pojisteni.objects.get(id=vyber_pojisteni)
        pojistenec.pojisteni.add(vyber_pojisteni)
      else:
        "UDELAT HLASKU, ZE NEBYLO NIC VYBRANO"
    messages.success(request, f"Nové pojištění bylo pojištěnci přidáno.")
    return redirect("pojistenci")
  
  return render(request, "pridat_pojisteni.html", {"pojistenec": pojistenec, "vsechna_pojisteni": vsechna_pojisteni})


# zaplaceno/nezaplaceno
def set_paid(request, pk):
  pojistenec = Pojistenec.objects.get(id=pk)
  pojistenec.isPaid = True if request.GET.get("isPaid") == "true" else False
  pojistenec.save()
  messages.success(request, "Stav byl upraven.")
  return redirect(reverse("pojistenci"))


#####
# CRUD POJISTENI
#####

# vytvoření view 
def vytvorit_pojisteni(request):
  if request.method == "POST":
    title = request.POST['title']
    nove_pojisteni = Pojisteni(title=title)
    nove_pojisteni.save()
    messages.success(request, "Nové pojištění bylo úspěšně vytvořeno.")
    return redirect("pojisteni")
    
  return render(request, "vytvorit_pojisteni.html")

# čtení view
@login_required(login_url= "/login")
def pojisteni(request):
  vsechna_pojisteni = Pojisteni.objects.all()
  pocet_pojisteni = Pojisteni.objects.count()

  # pagination = stránkování
  paginator = Paginator(vsechna_pojisteni, 5)
  page_number = request.GET.get("page")
  page_obj = paginator.get_page(page_number)

  return render(request, "pojisteni.html", {"vsechna_pojisteni": vsechna_pojisteni, "pocet_pojisteni": pocet_pojisteni, "page_obj": page_obj})


# smazání view
def odstranit_pojisteni(request, pk):
  pojisteni = Pojisteni.objects.get(id=pk)
  if request.method == "POST":
    pojisteni.delete()
    return redirect("pojisteni")
  return render(request, "odstranit_pojisteni.html", {"pojisteni": pojisteni})


# pojistná událost
def pojistna_udalost(request):
  uzivatel = request.user 

  if request.method == "POST":

    uzivatel = request.POST['uzivatel']
    predmet = request.POST['predmet']
    text_udalosti = request.POST['text_udalosti']

    send_mail(message=f'Uživatel "{uzivatel}" ti nahlásil tuto pojistnou událost:{text_udalosti}', 
              subject=f"{predmet}", 
              from_email=settings.EMAIL_HOST_USER, recipient_list=["tomasrec2@gmail.com"], 
              fail_silently= False)
    messages.success(request, "Pojistná událost byla administrátorovi odeslána na email.")
    return redirect("pojistenci")

  return render(request, "pojistna_udalost.html", {"uzivatel": uzivatel})





