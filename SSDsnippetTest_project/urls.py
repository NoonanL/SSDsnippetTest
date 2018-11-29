"""SSDsnippetTest_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from hello.views import myView
from django.views.generic.base import TemplateView
from django.conf.urls import url
from snippetTest.views import loginView, homeView, submitLogout, uploadSnippet, deleteSnippet, viewSnippets, editSnippet, openSnippet, searchSnippetsView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='login.html'),
        name='login'),
    path('admin/', admin.site.urls),
    path('sayHello/', myView),
    path('login/', loginView),
    path('submitLogin/', loginView),
    path('submitLogout/', submitLogout),
    path('home/', homeView),
    path('uploadSnippet/', uploadSnippet),
    path('deleteSnippet/<int:snippetId>/', deleteSnippet),
    path('viewSnippets/', viewSnippets),
    path('openSnippet/<int:snippetId>/', openSnippet),    
    path('editSnippet/<int:snippetId>/', editSnippet),
    path('searchSnippets/', searchSnippetsView),


]
