from django.shortcuts import render


def profile(request):
    """ Display the user's profile. """

    template = 'profiles/user_profile.html'
    context = {}

    return render(request, template, context)
