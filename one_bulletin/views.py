from django.shortcuts import render
from django.views.generic import ListView

from .models import NewsStory


class HomeView(ListView):
    template_name = "home.html"
    model = NewsStory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stories"] = NewsStory.objects.filter().order_by("-relevancy")[:50]
        return context
