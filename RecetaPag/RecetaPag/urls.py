"""
URL configuration for RecetaPag project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import RedirectView
from django import views
from RECETAPP import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='/index/')),
    path('index/', views.principal, name='principal'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("login/", views.login_view, name="login"),
    path("registro/", views.registro, name="registro"),
    path('pagprincipal/', views.pagprincipal, name='pagprincipal') ,
    path('recetas/', views.recetas, name='recetas'),
    path('mis-recetas/', views.mis_recetas, name='mis_recetas'),
    path('favorito/<int:id>/', views.agregar_a_favoritos, name='agregar_a_favoritos'),
    path('favoritas/', views.favoritas, name='favoritas'),
    path('crear-receta/', views.crear_receta, name='crear_receta'),
    path('editar-receta/<int:id>/', views.editar_receta, name='editar_receta'),
    path('eliminar-receta/<int:id>/', views.eliminar_receta, name='eliminar_receta'),
    path('receta/<int:receta_id>/', views.detalle_receta, name='detalle_receta'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
