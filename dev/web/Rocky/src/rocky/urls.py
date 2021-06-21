"""rocky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView

from home.views import HomeTemplateView, RegisterView, SugarCampView, NewDonationAPIView, TestTemplateView, RedirectViewTest
from accounts.views import CustomLoginView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', TemplateView.as_view(template_name = 'home.html')),
    url(r'^login', CustomLoginView.as_view()),
    url(r'^logout/$', logout_view),
    url(r'^register/$', RegisterView.as_view()),
    url(r'^test/$', TestTemplateView.as_view()),


    url(r'^share-usual/$', RedirectViewTest.as_view()),




    url(r'^contact/', TemplateView.as_view(template_name = 'snippets/contact.html')),
    url(r'^project-report/', TemplateView.as_view(template_name = 'snippets/project_report.html')),
    url(r'^why-rocky/', TemplateView.as_view(template_name = 'snippets/why_rocky.html')),


    url(r'^sugar-camp/', SugarCampView.as_view()),
    url(r'^api/sugar-camp/donation', NewDonationAPIView.as_view()),



    url(r'^accounts/', include('accounts.urls')),
    url(r'^vehicles/', include('vehicles.urls')),
    url(r'^tollgate/', include('tollgate.urls')),
    url(r'^billing/', include('billing.urls')),

    url(r'^idhl/', TemplateView.as_view(template_name = 'idhl.html')),
    url(r'^sidin-who-let-the-dork-out-chapter-18-novermber/', TemplateView.as_view(template_name = 'sidin.html')),


    #videos
    url(r'^project-videos/', TemplateView.as_view(template_name = 'videos/project_videos.html')),

]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



