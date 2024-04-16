from django.shortcuts import render, HttpResponse

# Create your views here.
def store(request):
    return render(request, "layouts/store.html")

def listing(request):
    return render(request, "layouts/listing.html")

def user(request):
    return render(request, "layouts/user.html")