from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Gig)
admin.site.register(Order)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(GigReview)
admin.site.register(SellerReview)
