from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.AthleteListView.as_view()),
    path('athletes', views.AthleteListView.as_view(), name='athletes'),
    path('athlete/<int:pk>', views.AthleteDetailView.as_view(), name='athlete_detail'),
    path('athlete/create',
        views.AthleteFormView.as_view(success_url=reverse_lazy('athletes')), name='athlete_create'),
    path('athlete/<int:pk>/update',
        views.AthleteFormView.as_view(success_url=reverse_lazy('athletes')), name='athlete_update'),
    path('athlete/<int:pk>/delete',
        views.AthleteDeleteView.as_view(success_url=reverse_lazy('athletes')), name='athlete_delete'),
    path('ad/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='athlete_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='athlete_comment_delete'),
]
