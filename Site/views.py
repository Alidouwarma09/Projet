from django.shortcuts import render, get_object_or_404
from Site.models import SiteParameters
from Utilisateurs.models import BlogPost


# Create your views here.
def Index(request):
    publication = BlogPost.objects.all()
    info_du_site = SiteParameters.objects.all()
    return render(request, 'index.html', {'info_du_site': info_du_site, 'publication': publication})


def publication_detail(request, pk):
    blog_posts = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'publication_detail.html', {'blog_posts': blog_posts})
