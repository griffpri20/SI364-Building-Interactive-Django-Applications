from django.shortcuts import render
from django.views import View
from django.views import generic

from unesco.models import site, category, iso, region, states

class SiteListView(generic.ListView):
    model = site

class SiteDetailView(generic.DetailView):
    model = site

class CategoryListView(generic.ListView):
    model = category

class CategoryDetailView(generic.DetailView):
    model = category

class IsoListView(generic.ListView):
    model = iso

class IsoDetailView(generic.DetailView):
    model = iso

class RegionListView(generic.ListView):
    model = region

class RegionDetailView(generic.DetailView):
    model = region

class StatesListView(generic.ListView):
    model = states

class statesDetailView(generic.DetailView):
    model = states
