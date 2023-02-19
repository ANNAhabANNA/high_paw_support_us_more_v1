from django.shortcuts import render, redirect, reverse
from .forms import ReviewForm
from django.contrib import messages
from django.views import generic, View
from .models import Review


def all_comments(request):
    """ Shows all comments posted """

    reviews = Review.objects.filter(status=1)
    context = {
        'reviews': reviews,
    }
    return render(request, 'reviews/all_comments.html', context)


class AddReview(View):
    """ Adds a comment """

    def get(self, request):
        template = 'reviews/add_comment.html'
        context = {'form': ReviewForm()}
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        title = form.instance.title

        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            messages.success(request, "Thank you! Your comment is submitted.")
            return redirect('home')
        else:
            messages.error(
                request, 'Failure! Please check if the form is valid.')
            context = {'form': form}
            return render(request, template, context)
