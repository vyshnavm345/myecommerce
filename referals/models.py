from django.db import models
from products.models import Custom_User
from referals.utils import generate_ref_code
# Create your models here.


class ReferenceProfile(models.Model):
    STATUS_CHOICES = [
        ('fulfilled', 'Fulfilled'),
        ('not_fulfilled', 'Not Fulfilled'),      
    ]
    
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(Custom_User, on_delete=models.CASCADE, blank=True, null=True, related_name="ref_by")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    first_purchase = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_fulfilled')

    
    def __str__(self) -> str:
        return f"{self.user.username}--{self.code}"
    
    def get_recommended_profiles(self):
        qs = ReferenceProfile.objects.all()
        my_recs = [p for p in qs if p.recommended_by == self.user]
        return my_recs
    
    def get_referal_link(self):
        return f"http://127.0.0.1:8000/referals/{self.code}"
    
    def save(self, *args, **kwargs):
        if self.code== '':
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)
    