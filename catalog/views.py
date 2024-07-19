from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "home.html")


def contacts(request):
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    message = request.POST.get("message")
    print(f"Имя: {name}, Тел.: {phone}\nСообщение: {message}")
    return render(request, "contacts.html")
