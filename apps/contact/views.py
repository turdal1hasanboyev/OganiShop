from django.shortcuts import render, redirect
from apps.contact.models import Contact
from apps.common.models import SubEmail


def contact(request):
    cat = request.GET.get('cat')
    search = request.GET.get('query')

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        Contact.objects.create(
            name=name,
            email=email,
            message=message,
        )

        return redirect('contact')
    
    if request.method == "POST":
        email = request.POST.get("subemail")
        SubEmail.objects.create(
            email=email,
        )

        return redirect ('contact')
    
    return render(request, 'contact.html')
