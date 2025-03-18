from django.contrib.auth.models import AbstractUser 
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import TextChoices
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True, verbose_name="Ảnh đại diện")
    ngay_sinh = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

class TheLoai(models.Model):
    ten = models.CharField(max_length=100, unique=True, verbose_name="Tên thể loại")

    def __str__(self):
        return self.ten

class DienVien(models.Model):
    ten = models.CharField(max_length=200, verbose_name="Tên diễn viên")

    def __str__(self):
        return self.ten

class TrangThaiPhim(TextChoices):
    SAP_CHIEU = "sap_chieu", "Sắp Chiếu"
    DANG_CHIEU = "dang_chieu", "Đang Chiếu"
    DA_KET_THUC = "da_ket_thuc", "Đã Kết Thúc"

class Movie(models.Model):
    ten_phim = models.CharField(max_length=200, verbose_name="Tên phim")
    video = models.FileField(upload_to="phim/videos/", null=True, blank=True, verbose_name="Video phim")
    the_loai = models.ManyToManyField(TheLoai, related_name="movies", verbose_name="Thể loại")
    mo_ta = models.TextField(verbose_name="Mô tả phim")
    dao_dien = models.CharField(max_length=200, verbose_name="Đạo diễn")
    dien_vien = models.ManyToManyField(DienVien, related_name="movies", verbose_name="Diễn viên")
    ngay_phat_hanh = models.DateField(null=True, blank=True, verbose_name="Ngày phát hành")
    thoi_luong = models.PositiveIntegerField(help_text="Thời lượng phim tính bằng phút", verbose_name="Thời lượng")
    anh_bia = models.ImageField(upload_to="phim/anhbia/", null=True, blank=True, verbose_name="Ảnh bìa")
    trailer = models.URLField(null=True, blank=True, verbose_name="Trailer")
    trang_thai = models.CharField(
        max_length=20,
        choices=TrangThaiPhim.choices,
        default=TrangThaiPhim.SAP_CHIEU,
        verbose_name="Trạng thái"
    )
    
    class Meta:
        ordering = ['-ngay_phat_hanh']

    def __str__(self):
        return self.ten_phim
    




class DanhGia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Người dùng")
    phim = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews", verbose_name="Phim")
    diem = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Điểm đánh giá")
    binh_luan = models.TextField(verbose_name="Bình luận")
    ngay_danh_gia = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đánh giá")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'phim'], name="unique_review_per_user")
        ]
        ordering = ['-ngay_danh_gia']

    def __str__(self):
        return f"{self.user.username} - {self.phim.ten_phim} ({self.diem})"

class LichSuXem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_history", verbose_name="Người dùng")
    phim = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watch_history", verbose_name="Phim")
    thoi_gian_bat_dau = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian bắt đầu")
    thoi_gian_ket_thuc = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian kết thúc")

    def __str__(self):
        return f"{self.user.username} đã xem {self.phim.ten_phim}"
