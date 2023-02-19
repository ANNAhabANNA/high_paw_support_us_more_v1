from django.shortcuts import render, redirect, reverse
from .forms import Contact
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import Contact
from .forms import ContactForm


# Create your views here
def index(request):

    """ Returns the index page """

    return render(request, 'home/index.html')


def contact(request):

    """ Returns the contact page """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        subject = request.POST['subject']
        message = request.POST['message']
        email = request.POST['email']
        sender = "Message from " + str(email)
        msg_mail = str(message) + ", " + str(sender)
        if form.is_valid():
            send_mail(
                subject,
                msg_mail,
                email,
                [settings.DEFAULT_FROM_EMAIL, ]
            )
            form.save()
            messages.success(request, 'Your email has been sent!')
            return redirect(reverse('contact'))
        else:
            messages.error(
                request,
                'Error. \
                    Please check your form is valid.'
            )
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'home/contact.html', context)
