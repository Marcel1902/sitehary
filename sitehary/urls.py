
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from hary.views import home, blog, blog_detail, create_blog, connexion, deconnexion, contacter
from sitehary import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('connexion/', connexion, name='connexion'),  # Nouvelle route pour la connexion
    path('logout/', deconnexion, name='logout'),
    path('blog/', blog, name='blog'),
    path('create_blog/', create_blog, name='create_blog'),
    path('blog_detail/<int:blog_id>', blog_detail, name='blog_detail'),
    path('contact/', contacter, name='contact'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
