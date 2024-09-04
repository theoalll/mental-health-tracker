from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2306165660',
        'name': 'Theo Ananda Lemuel',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)