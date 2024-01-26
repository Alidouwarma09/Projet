from django.shortcuts import render
from Site.models import SiteParameters


# Create your views here.
def Index(request):
    info_du_site = SiteParameters.objects.all()
    return render(request, 'index.html', {'info_du_site': info_du_site})
