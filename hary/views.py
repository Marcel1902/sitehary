from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import title
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

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


def contacter(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        sujet = request.POST.get("subject")
        message = request.POST.get("message")

        contenu_email = f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            # Envoi à toi (admin)
            send_mail(
                sujet,
                contenu_email,
                email,  # from_email
                ['faniloniainatanguymarcel@gmail.com'],
                fail_silently=False
            )

            # Confirmation à l'utilisateur (HTML avec logo)
            confirmation_sujet = "Confirmation de réception de votre message"
            confirmation_message = f"""
                <html>
                    <body style="font-family: 'Arial', sans-serif; margin: 0; padding: 0; background-color: #f5f5f5;">
                        <table role="presentation" style="width: 100%; background-color: #fab734; padding: 20px 0;">
                            <tr>
                                <td style="text-align: center; padding: 10px;">
                                    <img src="https://drive.google.com/uc?id=1k25Ado02yru9Ij0cc5NgAczRKUD-6BgZ" alt="Logo de l'Association" width="150" style="border-radius: 10px;"/>
                                </td>
                            </tr>
                        </table>
                        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                            <h2 style="color: #156183; font-size: 24px; text-align: center; margin-bottom: 20px;">Bonjour {nom},</h2>
                            <p style="color: #333; font-size: 16px; line-height: 1.5;">Nous avons bien reçu votre message et nous vous répondrons dans les plus brefs délais.</p>
                            <p style="color: #333; font-size: 16px; line-height: 1.5; margin-top: 20px;">
                                <strong>Voici un récapitulatif :</strong>
                            </p>
                            <p style="color: #333; font-size: 16px; line-height: 1.5;">
                                <strong>Sujet :</strong> {sujet}
                            </p>
                            <p style="color: #333; font-size: 16px; line-height: 1.5;">
                                <strong>Message :</strong><br>{message}
                            </p>
                            <br>
                            <p style="color: #333; font-size: 16px; line-height: 1.5;">Cordialement,</p>
                            <p style="color: #333; font-size: 16px; line-height: 1.5;">L’équipe de support</p>
                        </div>
                        <table role="presentation" style="width: 100%; background-color: #156183; padding: 10px 0; margin-top: 20px;">
                            <tr>
                                <td style="text-align: center;">
                                    <p style="color: #ffffff; font-size: 14px; margin: 0;">&copy; 2025 L’Association HARY</p>
                                </td>
                            </tr>
                        </table>
                    </body>
                </html>
            """

            send_mail(
                confirmation_sujet,
                "",  # Le message texte en texte brut n'est pas nécessaire ici, il est remplacé par `html_message`
                settings.DEFAULT_FROM_EMAIL,  # adresse de ton serveur mail
                [email],
                fail_silently=False,
                html_message=confirmation_message  # Le contenu HTML
            )

            messages.success(request, "Votre message a été envoyé avec succès.")
            return redirect('contact')

        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi : {str(e)}")

    return render(request, "hary/index.html")
        
        



