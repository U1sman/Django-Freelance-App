from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator, MaxValueValidator

STATUS_CHOICES = [
    ("active", "Active"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]

TIER_CHOICES = [
    ("BASIC", "Basic"),
    ("STANDARD", "Standard"),
    ("PREMIUM", "Premium"),
    ("CUSTOM", "Custom"),
]

class User(AbstractUser):
    bio= models.TextField(blank=True, max_length=1000)
    joined_date= models.DateField(auto_now_add=True)
    profile_pic= models.ImageField(default= "images/profile_pics/default_profile.jpg", upload_to="images/profile_pics/")
    skills= models.ManyToManyField("Skill", blank=True, related_name="users")
    country= CountryField(blank_label='(select country)', blank=True)
    languages= models.ManyToManyField("Language", blank=True, related_name="speakers")
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return f"Username: {self.username}, email:{self.email}"


class Gig(models.Model):
    related_seller= models.ForeignKey("User", related_name="gigs", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description= models.TextField(max_length=2000)
    cover_image= models.ImageField(upload_to="images/gig_covers/")
    category= models.ForeignKey("Category", related_name="gigs", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Title: {self.title} By: {self.related_seller.username}"


class Order(models.Model):
    buyer= models.ForeignKey("User", on_delete=models.CASCADE, related_name="orders")
    seller= models.ForeignKey("User", on_delete=models.CASCADE, related_name="orders_received")
    related_gig= models.ForeignKey("Gig", on_delete=models.CASCADE, related_name="gig_orders")
    price= models.DecimalField(max_digits=10, decimal_places=2)
    status= models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"RelatedGig: {self.related_gig.title} Buyer: {self.buyer.username} Status: {self.status}"


class Education(models.Model):
    related_user = models.ForeignKey("User", on_delete=models.CASCADE)
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)

    def __str__(self):
        return f"Person: {self.related_user.username} School: {self.school}, Degree:{self.degree}"


class Skill(models.Model):  
    name= models.CharField(unique=True, max_length=70)

    def  __str__(self):
        return f"{self.name}"


class Language(models.Model):
    name= models.CharField(max_length=100, unique=True)

    def  __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name= models.CharField(max_length=100, unique=True)

    def  __str__(self):
        return f"{self.name}"


class PricingPlan(models.Model):
    related_gig= models.ForeignKey("Gig", on_delete=models.CASCADE, related_name="pricing_plans")


class PricingOption(models.Model):
    related_pricingPlan= models.ForeignKey("PricingPlan", on_delete=models.CASCADE, related_name="pricing_options")
    type= models.CharField(choices=TIER_CHOICES, max_length=10)
    price= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_time= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    description= models.CharField(max_length=200)


class GigReview(models.Model):
    related_gig= models.ForeignKey("Gig", related_name="gig_reviews", on_delete=models.CASCADE)
    body= models.TextField(max_length=500)
    rating= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey("User", related_name="user_gig_reviews", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RelatedGig: {self.related_gig.title} author: {self.author.username} rating: {self.rating}"
    

class SellerReview(models.Model):
    related_seller= models.ForeignKey("User", related_name="seller_reviews", on_delete=models.CASCADE)
    body= models.TextField(max_length=500)
    rating= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author= models.ForeignKey("User", related_name="user_seller_reviews", on_delete= models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RelatedSeller: {self.related_seller.username} author: {self.author.username} rating: {self.rating}"