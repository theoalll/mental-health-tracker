from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required 

from django.shortcuts import render, redirect, reverse

from main.forms import MoodEntryForm
from main.models import MoodEntry

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

# use data from cookies
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

# Menambahkan Mood dengan AJAX
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# @login_required(login_url='/login') agar halaman main hanya dapat diakses oleh pengguna yang sudah login (terautentikasi)
@login_required(login_url='/login')
def show_main(request):
    mood_entries = MoodEntry.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'class': 'PBP D',
        'npm': '2306123456',
        'mood_entries': mood_entries,

        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        # menghubungkan satu mood entry dengan satu user melalui sebuah relationship
        mood_entry = form.save(commit=False) # mencegah Django agar tidak langsung menyimpan objek yang telah dibuat dari form langsung ke database
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)

@csrf_exempt # Django tidak perlu mengecek keberadaan csrf_token pada POST request yang dikirimkan
@require_POST # hanya bisa diakses ketika pengguna mengirimkan POST request ke fungsi tersebut. Jika pengguna mengirimkan request dengan method lain, maka dari Django akan dikembalikan eror 405 Method Not Allowed.
def add_mood_entry_ajax(request):
    mood = request.POST.get("mood")
    feelings = request.POST.get("feelings")
    mood_intensity = request.POST.get("mood_intensity")
    user = request.user

    new_mood = MoodEntry(
        mood=mood, 
        feelings=feelings,
        mood_intensity=mood_intensity,
        user=user
    )
    new_mood.save()

    return HttpResponse(b"CREATED", status=201)

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
      messages.error(request, "Invalid username or password. Please try again.")
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

# Menambahkan Fitur Edit Mood pada Aplikasi
def edit_mood(request, id):
    # Get mood entry berdasarkan id
    mood = MoodEntry.objects.get(pk = id)

    # Set mood entry sebagai instance dari form
    form = MoodEntryForm(request.POST or None, instance=mood)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_mood.html", context)

# Menambahkan Fitur Hapus Mood pada Aplikasi
def delete_mood(request, id):
    # Get mood berdasarkan id
    mood = MoodEntry.objects.get(pk = id)
    # Hapus mood
    mood.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))