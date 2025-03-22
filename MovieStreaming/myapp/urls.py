from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import search_movies, lich_su_xem, xem_phim

urlpatterns = [
    path('', views.home, name='home'),
    path("gioithieu/", views.gioithieu, name="gioithieu"),
    path('phim/onepiece/', views.onepiece, name='onepiece'),
    path('phim/kime/', views.kime, name='kime'),
    path('phim/natra/', views.natra, name='natra'),
    path('chitietphim/<int:id>/', views.chitietphim, name='chitietphim'),
    path("search/", search_movies, name="search_movies"),
    path('lich-su/', lich_su_xem, name='lich_su_xem'),
    
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
