from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.CookieListView.as_view()),
    path('cookies', views.CookieListView.as_view(), name='cookies'),
    path('cookie/<int:pk>', views.CookieDetailView.as_view(), name='cookie_detail'),
    path('cookie/create',
        views.CookieFormView.as_view(success_url=reverse_lazy('cookies')), name='cookie_create'),
    path('cookie/<int:pk>/update',
        views.CookieFormView.as_view(success_url=reverse_lazy('cookies')), name='cookie_update'),
    path('cookie/<int:pk>/delete',
        views.CookieDeleteView.as_view(success_url=reverse_lazy('cookies')), name='cookie_delete'),
    path('ad/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='cookie_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='cookie_comment_delete'),
]
