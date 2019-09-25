from stars.models import Star, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from stars.util import StarsListView, StarsDetailView, StarsCreateView, StarsUpdateView, StarsDeleteView
from stars.forms import CreateForm, CommentForm


class StarListView(StarsListView):
    model = Star
    template_name = "star_list.html"

class StarDetailView(StarsDetailView):
    model = Star
    template_name = "star_detail.html"

    def get(self, request, pk) :
        star = Star.objects.get(id=pk)
        comments = Comment.objects.filter(star=star).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'star' : star, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class StarCreateView(StarsCreateView):
    model = Star
    fields = ['name', 'distance', 'diameter']
    template_name = "star_form.html"
    success_url = reverse_lazy('stars')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add stars to the model before saving
        star = form.save(commit=False)
        star.owner = self.request.user
        star.save()
        return redirect(self.success_url)


class StarUpdateView(StarsUpdateView):
    model = Star
    fields = ['name', 'distance', 'diameter']
    template_name = "star_form.html"
    success_url = reverse_lazy('stars')
    def get(self, request, pk) :
        star = get_object_or_404(Star, id=pk, owner=self.request.user)
        form = CreateForm(instance=star)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        star = get_object_or_404(Star, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=star)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

class StarDeleteView(StarsDeleteView):
    model = Star
    template_name = "star_delete.html"


class StarFormView(LoginRequiredMixin, View):
    template = 'star_form.html'
    success_url = reverse_lazy('stars')

    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            star = get_object_or_404(Star, id=pk, owner=self.request.user)
            form = CreateForm(instance=star)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            star = get_object_or_404(Star, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=star)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Starjust the model stars before saving
        star = form.save(commit=False)
        star.owner = self.request.user
        star.save()
        return redirect(self.success_url)

class CommentCreateView(LoginRequiredMixin, View):
    template = 'star_form.html'
    success_url = reverse_lazy('stars')

    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        f = get_object_or_404(Star, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, star=f)
        comment.save()
        return redirect(reverse_lazy('star_detail', args=[pk]))

class CommentDeleteView(StarsDeleteView):
    model = Comment
    template_name = "star_comment_delete.html"

    def get_success_url(self) :
        star = self.object.star
        return reverse_lazy('star_detail', args=[star.id])
