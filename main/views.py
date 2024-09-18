from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required 

from django.shortcuts import render, redirect

from main.forms import MoodEntryForm
from main.models import MoodEntry

from django.http import HttpResponse
from django.core import serializers

# use data from cookies
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# @login_required(login_url='/login') agar halaman main hanya dapat diakses oleh pengguna yang sudah login (terautentikasi)
@login_required(login_url='/login')
def show_main(request):
    mood_entries = MoodEntry.objects.all()

    context = {
        'name': 'Pak Bepe',
        'class': 'PBP D',
        'npm': '2306123456',
        'mood_entries': mood_entries,

        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)

def show_xml(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Fungsi ini berfungsi untuk menghasilkan formulir registrasi secara otomatis dan menghasilkan akun pengguna ketika data di-submit dari form.
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

# Fungsi ini berfungsi untuk mengautentikasi pengguna yang ingin login
# authenticate(request, username=username, password=password) digunakan untuk melakukan autentikasi pengguna berdasarkan username dan password yang diterima dari permintaan (request) yang dikirim oleh pengguna saat login. Jika kombinasi valid, maka objek user akan di-return. Jika tidak, maka akan mengembalikan None.
# login(request, user) berfungsi untuk melakukan login terlebih dahulu. Jika pengguna valid, fungsi ini akan membuat session untuk pengguna yang berhasil login.
def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)

            # menambahkan fungsionalitas menambahkan cookie yang bernama last_login untuk melihat kapan terakhir kali pengguna melakukan login.
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))

            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

# Fungsi ini berfungsi untuk melakukan mekanisme logout
# logout(request) digunakan untuk menghapus sesi pengguna yang saat ini masuk.
# return redirect('main:login') mengarahkan pengguna ke halaman login dalam aplikasi Django.
def logout_user(request):
    logout(request)

    # menghapus cookie last_login saat user melakukan logout.
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')

    return response