from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .models import Movie

def home(request):
    one_piece = Movie.objects.filter(ten_phim__icontains="One Piece").first()
    attack_on_titan = Movie.objects.filter(ten_phim__icontains="Attack on Titan").first()

    context = {
        "highlighted_movies": [one_piece, attack_on_titan]
    }
    return render(request, "myapp/home.html", context)



def gioithieu(request):
    return render(request, 'myapp/gioithieu.html')