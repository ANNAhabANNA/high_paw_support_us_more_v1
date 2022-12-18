from django.shortcuts import render, redirect, reverse
from .forms import ReviewForm
from django.contrib import messages
from django.views import generic, View
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Review
from .forms import ReviewForm, ApproveForm


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
            messages.error(request, 'Failure! Please check if the form is valid.')
            context = {'form': form}
            return render(request, template, context)


class ModerateDeleteReview(DeleteView):
    """ Deletes a comment """

    model = Review
    template_name = 'reviews/delete_comment.html'
    success_url = reverse_lazy('moderate_comment')


class ModerateApproveReview(UpdateView):
    """ Updates a comment from draft to approved """

    model = Review
    template_name = 'reviews/approve_comment.html'
    form_class = ApproveForm
    success_url = reverse_lazy('moderate_comment')


class ModerateReviews(generic.ListView):
    """ Shows comment awaiting approval """
    template_name = 'reviews/moderate_comment.html'
    model = Review
    context_object_name = 'comments'

    def get_queryset(self):
        return Review.objects.filter(status=0).order_by('-date_created')


class ModerateUpdateReview(UpdateView):
    """ Updates a review """
    model = Review
    template_name = 'reviews/update_comment.html'
    form_class = ReviewForm
    success_url = reverse_lazy('moderate_comment')
