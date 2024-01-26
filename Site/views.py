from django.shortcuts import render
from Site.models import SiteParameters
from Utilisateurs.models import BlogPost


# Create your views here.
def Index(request):
    publication=BlogPost.objects.all()
    info_du_site = SiteParameters.objects.all()
    return render(request, 'index.html', {'info_du_site': info_du_site, 'publication': publication})
