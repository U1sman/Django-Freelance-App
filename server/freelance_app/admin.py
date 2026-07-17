from django.contrib import admin
from .models import *

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#     'id', 'username', 'email', 'first_name', 'last_name',
#     'bio', 'tagline', 'joined_date', 'profile_pic', 's'
#     'is_seller', 'country',
#     )
    

# class GigAdmin(admin.ModelAdmin):
#     list_display = (
#     'id', 'title', 'description', 'cover_image',
#     'related_seller', 'category', 'created_on',
#     )


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#     'id', 'buyer', 'seller', 'related_gig',
#     'related_pricing_option', 'requirements',
#     'status', 'created_on',
#     )


admin.site.register(User)
admin.site.register(Gig)
admin.site.register(Order)
admin.site.register(OrderActivity)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Category)
admin.site.register(PricingOption)
admin.site.register(GigReview)
admin.site.register(SellerReview)
admin.site.register(Delivery)
admin.site.register(DeliveryAttachment)
admin.site.register(Offer)
admin.site.register(Quotation)
admin.site.register(RevisionRequest)
