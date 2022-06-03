from django.shortcuts import render
from django.views.generic import ListView

from .models import NewsStory


# respond to requests by serving template home.html
# with 50 most relevant news stories currently in database
class HomeView(ListView):
    template_name = "home.html"
    model = NewsStory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stories"] = NewsStory.objects.filter().order_by("-relevancy")[:50]
        return context
