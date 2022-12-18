from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_comments, name='all_comments'),
    path('add_comment/', views.AddReview.as_view(), name='add_comment'),
    path('moderate_comment/', views.ModerateReviews.as_view(),name='moderate_comment'),
    path('reviews/<slug:slug>/approve_comment', views.ModerateApproveReview.as_view(), name='approve_comment'),
    path('reviews/admin_update_comment/<slug:slug>', views.ModerateUpdateReview.as_view(), name='moderate_update_comment'),
    path('reviews/<slug:slug>/admin_delete_comment/', views.ModerateDeleteReview.as_view(), name='moderate_delete_comment'),
]