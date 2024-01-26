# admin/views.py
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.views import View

from Site.forms import SiteParametersForm
from Utilisateurs.models import CustomUser, Message, BlogPost
from Utilisateurs.forms import UserRegistrationForm, MessageForm, BlogPostForm, DeactivateUserForm, ActivateUserForm
from django.db.models import Q
from Site.models import SiteParameters, Visitor


@login_required(login_url='utilisateurs:connexion')
def admin_dashboard(request):
    utilisateurs = CustomUser.objects.all()
    return render(request, 'dashboard.html', {'utilisateurs': utilisateurs})


@login_required(login_url='utilisateurs:connexion')
def admin_create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Utilisateur ajouter avec succès.")
            return redirect('admin:admin_create_user')
    else:
        form = UserRegistrationForm()
    return render(request, 'add_utilisateur.html', {'form': form})


@login_required(login_url='utilisateurs:connexion')
def admin_edit_user(request, user_id):
    utilisateur = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES, instance=utilisateur)
        if form.is_valid():
            form.save()
            return redirect('admin:admin_dashboard')

    else:
        form = UserRegistrationForm(instance=utilisateur)

    return render(request, 'user_list.html', {'form': form, 'utilisateur': utilisateur})


@login_required(login_url='utilisateurs:connexion')
def admin_delete_user(request, user_id):
    utilisateur = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, f"Vous avez supprimé l'utilisateur {utilisateur.nom} avec succès.")
        return HttpResponseRedirect(reverse('admin:tous_les_user'))

    return render(request, 'delete_user.html', {'utilisateur': utilisateur})


@login_required(login_url='utilisateurs:connexion')
@user_passes_test(lambda u: u.role == 'admin')
def tous_les_user(request):
    utilisateurs = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'all_users': utilisateurs})


@login_required(login_url='utilisateurs:connexion')
@user_passes_test(lambda u: u.role == 'admin')
def utilisateur(request):
    utilisateurs = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'utlisateurs.html', {'all_users': utilisateurs})


@login_required(login_url='utilisateurs:connexion')
def Messages(request, user_id):
    recipient = get_object_or_404(CustomUser, id=user_id)
    messages = CustomUser.objects.get_user_messages(request.user, recipient)

    # Marquer tous les messages comme lus lorsqu'ils sont chargés
    unread_messages = messages.filter(is_read=False)

    if unread_messages.exists():
        # Utiliser bulk_update pour marquer tous les messages non lus comme lus
        Message.objects.filter(Q(pk__in=unread_messages.values_list('pk', flat=True))).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Message.objects.create(sender=request.user, receiver=recipient, content=content)

            return redirect('admin:messages', user_id=user_id)
    else:
        form = MessageForm()

    context = {
        'recipient': recipient,
        'messages': messages,
        'form': form,
    }

    return render(request, 'messages.html', context)


@login_required(login_url='utilisateurs:connexion')
def Create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('admin:post')
    else:
        form = BlogPostForm()

    return render(request, 'publication/create_blog.html', {'form': form})


class BlogPostDetailView(View):
    def get(self, request, blog_id):
        blog_post = get_object_or_404(BlogPost, id=blog_id)
        return render(request, 'blog_post_detail.html', {'blog_post': blog_post})


@login_required(login_url='utilisateurs:connexion')
def blog_list(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        blog_id = request.POST.get('blog_id')
        blog_post = get_object_or_404(BlogPost, id=blog_id)

        if request.user not in blog_post.likes.all():
            blog_post.likes.add(request.user)

        like_count = blog_post.likes.count()
        return JsonResponse({'like_count': like_count})

    # Récupérer tous les articles de blog
    blog_posts = BlogPost.objects.all()

    # Incrémenter le compteur de vues pour chaque article de blog
    for blog_post in blog_posts:
        blog_post.increment_views()

    return render(request, 'publication/post.html', {'blog_posts': blog_posts})


@login_required(login_url='utilisateurs:connexion')
def share_post(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    blog_post.shares += 1
    blog_post.save()
    return redirect('blog:blog_detail', blog_id=blog_id)


@login_required(login_url='utilisateurs:connexion')
def All_Blog(request):
    tout_les_blog = BlogPost.objects.all()
    return render(request, 'publication/tout_les_blog.html', {'tout_les_blog': tout_les_blog})


@login_required(login_url='utilisateurs:connexion')
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    return redirect('admin:All_Blog')


@login_required(login_url='utilisateurs:connexion')
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('admin:All_Blog')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'publication/edit_post.html', {'form': form, 'post': post})


def view_blog(request, post_id):
    tout_les_blog = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'publication/view_blog.html', {'tout_les_blog': tout_les_blog})


@login_required
def active_utilisateur(request, utilisateur_id):
    if request.method == 'POST':
        utilisateur = get_object_or_404(CustomUser, id=utilisateur_id)
        utilisateur.is_active = True
        utilisateur.save()
        print("active")
        return redirect('admin:tous_les_user')


@login_required
def desactive_utilisateur(request, utilisateur_id):
    if request.method == 'POST':
        utilisateur = get_object_or_404(CustomUser, id=utilisateur_id)
        utilisateur.is_active = False
        utilisateur.save()
        print("deactive")
        return redirect('admin:tous_les_user')


@login_required(login_url='utilisateurs:connexion')
def Info_du_site(request):
    info_du_site = SiteParameters.objects.all()
    total_visitors = Visitor.objects.count()
    return render(request, 'parametre_du_site/info_du_site.html',
                  {'info_du_site': info_du_site, 'total_visitors': total_visitors})


@login_required(login_url='utilisateurs:connexion')
def modifier_parametres(request, pk):
    site_info = SiteParameters.objects.get(pk=pk)

    if request.method == 'POST':
        form = SiteParametersForm(request.POST, request.FILES, instance=site_info)
        if form.is_valid():
            form.save()
            print("Success")
            return redirect('admin:info_du_site')
        else:
            print("Error", form.errors)
    else:
        form = SiteParametersForm(instance=site_info)

    return render(request, 'parametre_du_site/info_du_site.html', {'form': form, 'site_info': site_info})
