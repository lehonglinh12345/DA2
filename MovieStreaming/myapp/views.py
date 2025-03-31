from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Movie


from .models import Movie, User, TheLoai, LichSuXem

# Trang chủ và giới thiệu
def home(request):
    return render(request, "myapp/pages/home.html")
def home1(request):
    return render(request, "myapp/pages/home1.html")
def gioithieu(request):
    return render(request, 'myapp/pages/gioithieu.html')

# Chi tiết phim
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
    video_embed = movie.video_url.replace("watch?v=", "embed/") if movie.video_url and "watch?v=" in movie.video_url else movie.video_url
    return render(request, 'myapp/pages/chitietphim.html', {'movie': movie})

# Chức năng đăng nhập
def login_view(request):   
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email hoặc mật khẩu không đúng!')
            return render(request, 'myapp/log/login.html', {'email': email})

    return render(request, 'myapp/log/login.html')

@login_required
def profile(request):
    return render(request, "myapp/log/profile.html")

# Chức năng tìm kiếm phim
def search_movies(request):
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(ten_phim__icontains=query)
    if genre:
        movies = movies.filter(the_loai__ten__icontains=genre)

    return render(request, "myapp/search/search_results.html", {"movies": movies.distinct(), "query": query, "genre": genre})

# Chức năng xem phim
@login_required
def xem_phim(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'myapp/pages/xem_phim.html', {'movie': movie})

@login_required
def lich_su_xem(request):
    lich_su = LichSuXem.objects.all().order_by('-thoi_gian_bat_dau')
    return render(request, 'myapp/lichsu/lich_su_xem.html', {'lich_su': lich_su})

@login_required
def xem_phim_luu_lich_su(request, phim_id):
    phim = get_object_or_404(Movie, id=phim_id)
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

# Cập nhật thông tin cá nhân
@csrf_exempt
@login_required
def update_fullname(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_fullname = data.get("fullname")
            user = request.user
            user.fullname = new_fullname
            user.save()
            return JsonResponse({"success": True, "fullname": new_fullname})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})

def phim_sap_chieu(request):
    upcoming_movies = Movie.objects.filter(trang_thai='Sắp Chiếu')  

    # 🛠 In log để kiểm tra dữ liệu
    print("🔥 DEBUG: Số lượng phim sắp chiếu:", upcoming_movies.count())
    for movie in upcoming_movies:
        print(f"🎬 {movie.ten_phim} - {movie.trang_thai}")

    context = {'upcoming_movies': upcoming_movies}
    return render(request, 'myapp/pages/home1.html', context)
