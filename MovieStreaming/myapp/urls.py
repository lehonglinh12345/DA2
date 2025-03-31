from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, include  
from .views import search_movies, lich_su_xem, xem_phim
from myapp.views import login_view
from django.views.generic import TemplateView
from .views import update_fullname, phim_sap_chieu


urlpatterns = [
    path("", TemplateView.as_view(template_name="myapp/pages/home.html"), name="home"), 
    path('accounts/', include('allauth.urls')),
    path("gioithieu/", views.gioithieu, name="gioithieu"),
    path('phim/onepiece/', views.onepiece, name='onepiece'),
    path('phim/kime/', views.kime, name='kime'),
    path('phim/natra/', views.natra, name='natra'),
    path('log/login/', login_view, name='login'),
    path('log/profile/', views.profile, name='profile'),
    path('chitietphim/<int:id>/', views.chitietphim, name='chitietphim'),
    path("search/", search_movies, name="search_movies"),
    path('lich-su/', lich_su_xem, name='lich_su_xem'),
    path("update-fullname/", update_fullname, name="update_fullname"),
    path('phim-sap-chieu/', phim_sap_chieu, name='phim_sap_chieu'), 
    
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
