from django.shortcuts import render, HttpResponse

# Create your views here.
def store(request):
    return render(request, "Layouts/store.html")

def listing(request):
    return render(request, "Layouts/listing.html")

def user(request):
    return render(request, "Layouts/user.html")