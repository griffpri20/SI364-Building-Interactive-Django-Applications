from athletes.models import Athlete, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from athletes.util import AthletesListView, AthletesDetailView, AthletesCreateView, AthletesUpdateView, AthletesDeleteView
from athletes.forms import CreateForm, CommentForm


class AthleteListView(AthletesListView):
    model = Athlete
    template_name = "athlete_list.html"

class AthleteDetailView(AthletesDetailView):
    model = Athlete
    template_name = "athlete_detail.html"

    def get(self, request, pk) :
        athlete = Athlete.objects.get(id=pk)
        comments = Comment.objects.filter(athlete=athlete).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'athlete' : athlete, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class AthleteCreateView(AthletesCreateView):
    model = Athlete
    fields = ['name', 'description', 'experience']
    template_name = "athlete_form.html"
    success_url = reverse_lazy('athletes')
    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Add athletes to the model before saving
        athlete = form.save(commit=False)
        athlete.owner = self.request.user
        athlete.save()
        return redirect(self.success_url)


class AthleteUpdateView(AthletesUpdateView):
    model = Athlete
    fields = ['name', 'description', 'experience']
    template_name = "athlete_form.html"
    success_url = reverse_lazy('athletes')
    def get(self, request, pk) :
        athlete = get_object_or_404(Athlete, id=pk, owner=self.request.user)
        form = CreateForm(instance=athlete)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        athlete = get_object_or_404(Athlete, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=athlete)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

class AthleteDeleteView(AthletesDeleteView):
    model = Athlete
    template_name = "athlete_delete.html"


class AthleteFormView(LoginRequiredMixin, View):
    template = 'athlete_form.html'
    success_url = reverse_lazy('athletes')

    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            athlete = get_object_or_404(Athlete, id=pk, owner=self.request.user)
            form = CreateForm(instance=athlete)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            athlete = get_object_or_404(Athlete, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=athlete)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Athletejust the model athletes before saving
        athlete = form.save(commit=False)
        athlete.owner = self.request.user
        athlete.save()
        return redirect(self.success_url)

class CommentCreateView(LoginRequiredMixin, View):
    template = 'athlete_form.html'
    success_url = reverse_lazy('athletes')

    def get(self, request, pk=None) :
        form = CreateForm()
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk) :
        f = get_object_or_404(Athlete, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, athlete=f)
        comment.save()
        return redirect(reverse_lazy('athlete_detail', args=[pk]))

class CommentDeleteView(AthletesDeleteView):
    model = Comment
    template_name = "athlete_comment_delete.html"

    def get_success_url(self) :
        athlete = self.object.athlete
        return reverse_lazy('athlete_detail', args=[athlete.id])
