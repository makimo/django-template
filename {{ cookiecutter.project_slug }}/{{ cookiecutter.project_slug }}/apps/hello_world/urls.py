from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('world/', TemplateView.as_view(template_name='hello_world.html'))
]
