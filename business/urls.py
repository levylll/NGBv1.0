from django.conf.urls import url
from business.views import FilmPackView
from django.views.generic import TemplateView,DetailView
from blog.models import News

urlpatterns = [
        #add by levy @20150611
        url(r'^productpack/$',FilmPackView.as_view()),
        #add end
]
