from cookies.models import Cookie, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from cookies.util import CookiesListView, CookiesDetailView, CookiesCreateView, CookiesUpdateView, CookiesDeleteView
from cookies.forms import CreateForm, CommentForm


class CookieListView(CookiesListView):
    model = Cookie
    template_name = "cookie_list.html"

class CookieDetailView(CookiesDetailView):
    model = Cookie
    template_name = "cookie_detail.html"

    def get(self, request, pk) :
        cookie = Cookie.objects.get(id=pk)
        comments = Comment.objects.filter(cookie=cookie).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'cookie' : cookie, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class CookieCreateView(CookiesCreateView):
    model = Cookie
    fields = ['name', 'description', 'experience']
    template_name = "cookie_form.html"
    success_url = reverse_lazy('cookies')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add cookies to the model before saving
        cookie = form.save(commit=False)
        cookie.owner = self.request.user
        cookie.save()
        return redirect(self.success_url)


class CookieUpdateView(CookiesUpdateView):
    model = Cookie
    fields = ['name', 'description', 'experience']
    template_name = "cookie_form.html"
    success_url = reverse_lazy('cookies')
    def get(self, request, pk) :
        cookie = get_object_or_404(Cookie, id=pk, owner=self.request.user)
        form = CreateForm(instance=cookie)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        cookie = get_object_or_404(Cookie, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=cookie)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

class CookieDeleteView(CookiesDeleteView):
    model = Cookie
    template_name = "cookie_delete.html"


class CookieFormView(LoginRequiredMixin, View):
    template = 'cookie_form.html'
    success_url = reverse_lazy('cookies')

    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            cookie = get_object_or_404(Cookie, id=pk, owner=self.request.user)
            form = CreateForm(instance=cookie)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            cookie = get_object_or_404(Cookie, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=cookie)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Cookiejust the model cookies before saving
        cookie = form.save(commit=False)
        cookie.owner = self.request.user
        cookie.save()
        return redirect(self.success_url)

class CommentCreateView(LoginRequiredMixin, View):
    template = 'cookie_form.html'
    success_url = reverse_lazy('cookies')

    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        f = get_object_or_404(Cookie, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, cookie=f)
        comment.save()
        return redirect(reverse_lazy('cookie_detail', args=[pk]))

class CommentDeleteView(CookiesDeleteView):
    model = Comment
    template_name = "cookie_comment_delete.html"

    def get_success_url(self) :
        cookie = self.object.cookie
        return reverse_lazy('cookie_detail', args=[cookie.id])
