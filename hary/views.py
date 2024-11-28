from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import title

from .models import Activity, Event, Blog


# Create your views here.
def home(request):
    activities = Activity.objects.all()
    events = Event.objects.all()
    # Récupérer les trois derniers articles
    derniers_articles = Blog.objects.all().order_by('-created')[:3]
    context = {"activities": activities, "events": events, "derniers_articles": derniers_articles}
    return render(request, 'hary/index.html', context=context)

def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Utilisez request.FILES pour récupérer l'image téléchargée
        blog = Blog(title=title, content=content, image=image, user=request.user)
        blog.save()
        return redirect('blog')  # Redirigez vers la liste des blogs après l'ajout
    return render(request, 'hary/blog.html')
def connexion(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            # Authentifie l'utilisateur et redirige vers la page d'accueil
            login(request, user)
            return redirect('blog')
        else:
            return render(request, 'hary/connexion.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect'})
    return render(request, 'hary/blog.html')

def deconnexion(request):
    # Déconnecte l'utilisateur et redirige vers la page de connexion
    logout(request)
    return redirect('blog')

def blog(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 6)  # 10 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hary/blog.html', {'page_obj': page_obj})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Vérifier si l'utilisateur a déjà vu cet article
    if not request.session.get(f'viewed_blog_{blog_id}', False):
        blog.calculer_nb_vue()
        request.session[f'viewed_blog_{blog_id}'] = True

    return render(request, 'hary/blog_detail.html', {'blog': blog})



