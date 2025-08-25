from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Group(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mod_groups'
        ordering = ['title']

    def __str__(self):
        return self.title

class Item(models.Model):
    STATUS = [
        ('draft', 'Nháp'),
        ('live', 'Công khai'),
        ('off', 'Ngưng bán'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='items')
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    stars = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    status = models.CharField(max_length=10, choices=STATUS, default='draft')
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mod_items'
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def final_price(self):
        return self.discount if self.discount else self.cost

    @property
    def is_available(self):
        return self.quantity > 0

class Feedback(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    message = models.TextField()
    verified = models.BooleanField(default=False)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mod_feedbacks'
        ordering = ['-posted_on']
        unique_together = ('item', 'user')

    def __str__(self):
        return f"{self.user.username} đánh giá {self.item.title}"

class Purchase(models.Model):
    STATUSES = [
        ('wait', 'Đợi duyệt'),
        ('ship', 'Đang giao'),
        ('done', 'Hoàn tất'),
        ('fail', 'Đã huỷ'),
    ]

    code = models.CharField(max_length=20, unique=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUSES, default='wait')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mod_purchases'
        ordering = ['-created_on']

    def __str__(self):
        return f"Đơn hàng #{self.code}"
