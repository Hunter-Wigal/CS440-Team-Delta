from django.shortcuts import render, HttpResponse

# Create your views here.
def store(request):
    return render(request, "layouts/store.html")

def listing(request):
    return render(request, "layouts/listing.html")

def account(request):
    return render(request, "layouts/account.html")

def inventory(request):
    return render(request, "layouts/inventory.html")