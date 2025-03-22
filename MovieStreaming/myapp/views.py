from django.shortcuts import render, get_object_or_404
from .models import Movie


def home(request):
  
    return render(request, "myapp/pages/home.html")

def gioithieu(request):
    return render(request, 'myapp/pages/gioithieu.html')

def onepiece(request):
    movie = get_object_or_404(Movie, ten_phim="One Piece") 
    return render(request, 'myapp/pages/phim/onepiece.html', {'movie': movie})
def kime(request):
    movie = get_object_or_404(Movie, ten_phim="Kimetsu no Yaiba") 
    return render(request, 'myapp/pages/phim/kime.html', {'movie': movie})
def natra(request):
    movie = get_object_or_404(Movie, ten_phim="NaTra2") 
    return render(request, 'myapp/pages/phim/natra.html', {'movie': movie})

def chitietphim(request, id):  
    movie = get_object_or_404(Movie, id=id)
     
    if movie.video_url and "watch?v=" in movie.video_url:
      video_embed = movie.video_url.replace("watch?v=", "embed/")
    else:
      video_embed = movie.video_url
 
    return render(request, 'myapp/pages/chitietphim.html', {'movie': movie})


from .models import Movie, TheLoai

def search_movies(request):
    query = request.GET.get("q", "").strip()  # Lấy từ khóa tìm kiếm
    genre = request.GET.get("genre", "").strip()  # Lấy thể loại nếu có

    movies = Movie.objects.all()

    if query:
        movies = movies.filter(ten_phim__icontains=query)

    if genre:
        movies = movies.filter(the_loai__ten__icontains=genre)

    context = {
        "movies": movies.distinct(),  # Tránh trùng lặp nếu có nhiều thể loại
        "query": query,
        "genre": genre,
    }
    return render(request, "myapp/search/search_results.html", context)



from django.contrib.auth.decorators import login_required
from .models import LichSuXem

@login_required
def lich_su_xem(request):
    lich_su = LichSuXem.objects.all().order_by('-thoi_gian_bat_dau')
    return render(request, 'myapp/lichsu/lich_su_xem.html', {'lich_su': lich_su})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import JsonResponse
from .models import Movie, LichSuXem


@login_required
def xem_phim(request, phim_id):
    phim = get_object_or_404(Movie, id=phim_id)

    # Lưu vào lịch sử xem
    lich_su, created = LichSuXem.objects.get_or_create(
        user=request.user,
        phim=phim,
        defaults={'thoi_gian_bat_dau': now()}
    )

    if not created:
        lich_su.thoi_gian_bat_dau = now()
        lich_su.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'message': 'Lịch sử đã được cập nhật!', 'status': 'success'})

    return render(request, 'xem_phim.html', {'phim': phim})


def xem_phim(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'myapp/pages/xem_phim.html', {'movie': movie})

