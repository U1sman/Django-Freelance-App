from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator, MaxValueValidator
import uuid
from django.db.models import TextChoices
from languages_plus.models import Language
from decimal import Decimal 
from datetime import datetime, timedelta


class User(AbstractUser):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    bio= models.TextField(blank=True, max_length=1000)
    tagline= models.CharField(blank=True, max_length=100)
    profile_pic= models.ImageField(default= "images/profile_pics/default_profile.jpg", upload_to="images/profile_pics/")
    skills= models.ManyToManyField("Skill", blank=True, related_name="users")
    country= CountryField(blank_label='(select country)', blank=True)
    languages= models.ManyToManyField(Language, blank=True,related_name='speakers') 
    is_seller= models.BooleanField(default=False)

    def __str__(self):
        return f"Username: {self.username}, email:{self.email}"


class Gig(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    related_seller= models.ForeignKey("User", related_name="gigs", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, validators=[MinLengthValidator(15, message="Title must be atleast 15 characters long")])
    description= models.TextField(max_length=2000, validators=[MinLengthValidator(50, message="Description must be at least 50 characters long.")])  
    thumbnail= models.ImageField(upload_to="images/gig_covers/", blank=True, null=True)
    category= models.ForeignKey("Category", related_name="gigs", on_delete=models.SET_NULL, null=True)
    created_on= models.DateTimeField(auto_now_add=True)
    allow_custom_offers = models.BooleanField(default=False, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('1.00'), message="Starting price cannot be less than $1.00.")])
    
    def __str__(self):
        return f"Title: {self.title} By: {self.related_seller.username}"


class Order(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        OVERDUE = 'OVERDUE', 'Overdue'

    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    buyer= models.ForeignKey("User", on_delete=models.PROTECT, related_name="orders")
    seller= models.ForeignKey("User", on_delete=models.PROTECT, related_name="orders_received")
    related_gig= models.ForeignKey("Gig", on_delete=models.SET_NULL, null=True, related_name="gig_orders")
    related_pricing_option= models.ForeignKey("PricingOption", on_delete=models.SET_NULL, related_name="orders", null=True, blank=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField(max_length=3000)
    status= models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    delivery_days= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)]) 
    reqs_submitted_at= models.DateTimeField(auto_now_add=True, null= True, blank=True) 
    placed_at= models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.due_at:
            self.due_at = timezone.now() + timedelta(days=self.delivery_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"RelatedGig: {self.related_gig.title} Seller: {self.seller.username} Status: {self.status}"


class OrderActivity(models.Model):
    related_order= models.ForeignKey("Order", on_delete=models.CASCADE, related_name="activities", null=True, blank=True)
    details= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order: {self.related_order}"


class Education(models.Model):
    related_user= models.ForeignKey("User", on_delete=models.CASCADE)
    school= models.CharField(max_length=255)
    degree= models.CharField(max_length=255)

    def __str__(self):
        return f"Person: {self.related_user.username} School: {self.school}, Degree:{self.degree}"


class Skill(models.Model):  
    name= models.CharField(unique=True, max_length=70)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name= models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"


class PricingOption(models.Model):
    class Tier(models.TextChoices):
        BASIC = 'BASIC', 'Basic'
        STANDARD = 'STANDARD', 'Standard'
        PREMIUM = 'PREMIUM', 'Premium'

    related_gig= models.ForeignKey("Gig", on_delete=models.CASCADE, related_name="pricing_options", null= True, blank=True)
    tier= models.CharField(choices=Tier.choices, max_length=10)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    description= models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"({self.tier}) Pricing Option for {self.related_gig}"


class GigReview(models.Model):
    related_gig= models.ForeignKey("Gig", related_name="gig_reviews", on_delete= models.CASCADE)
    related_order= models.OneToOneField("Order", related_name="review", on_delete= models.CASCADE)
    body= models.TextField(max_length=500)
    rating= models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.ForeignKey("User", related_name="gig_review_author", on_delete= models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"RelatedGig: {self.related_gig.title} author: {self.author.username} rating: {self.rating}"
    

class SellerReview(models.Model):
    related_seller= models.ForeignKey("User", related_name="seller_reviews", on_delete=models.CASCADE)
    body= models.TextField(max_length=500)
    rating= models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author= models.ForeignKey("User", related_name="user_seller_reviews", on_delete= models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):    
        return f"RelatedSeller: {self.related_seller.username} author: {self.author.username} rating: {self.rating}"
    

class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'

    related_order= models.ForeignKey("Order", on_delete=models.CASCADE, related_name="deliveries")
    message= models.TextField(max_length=500)
    sender= models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="deliveries")
    status= models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    delivered_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery for ORDER: {self.related_order.id} STATUS: {self.status}"


class DeliveryAttachment(models.Model):
    related_delivery= models.ForeignKey("Delivery", on_delete=models.CASCADE, related_name="attachments")
    file_url= models.FileField(upload_to='files/deliveries/', null=True, blank=True)
    file_size= models.PositiveIntegerField(null=True, blank=True)
    file_type= models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.file_url:
            self.file_size = self.file_url.size
            self.file_type = self.file_url.file.content_type if hasattr(self.file_url.file, 'content_type') else None
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Attachment for Delivery #{self.related_delivery.id}"
    

class Offer(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'ACCEPTED','Accepted'
        REJECTED = 'REJECTED','Rejected'
        PENDING_RESPONSE = 'PENDING_RESPONSE','Pending Response'
        QUOTED = 'QUOTED','Quoted'
    status= models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_RESPONSE)
    requirements = models.TextField(max_length=3000)
    delivery_days= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    related_gig= models.ForeignKey("Gig", on_delete=models.CASCADE, related_name="offers")
    sender= models.ForeignKey("User", on_delete=models.CASCADE, related_name="offers_sent")
    receiver= models.ForeignKey("User", on_delete=models.CASCADE, related_name="offers_received")
    sent_at= models.DateTimeField(auto_now_add=True)
    responded_at= models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Offer for Gig: {self.related_gig.title}"


class Quotation(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = 'ACCEPTED','Accepted'
        REJECTED = 'REJECTED','Rejected'
        PENDING_RESPONSE = 'PENDING_RESPONSE','Pending_Response'
    status= models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_RESPONSE)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    remarks= models.TextField(max_length=1000)  
    delivery_days= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    related_offer= models.OneToOneField("Offer", on_delete=models.CASCADE, related_name="quotations")
    sent_at= models.DateTimeField(auto_now_add=True)
    responded_at= models.DateTimeField(null=True, blank=True)
    sender= models.ForeignKey("User", on_delete=models.CASCADE, related_name="quotations_sent")
    receiver= models.ForeignKey("User", on_delete=models.CASCADE, related_name="quotations_received")

    def __str__(self):
        return f"Quotation for Gig: {self.related_offer.related_gig.title}"


class RevisionRequest(models.Model):
    related_order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="revisions")
    related_delivery = models.OneToOneField("Delivery", on_delete=models.CASCADE, related_name="revision_request")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    requirements = models.TextField(max_length=2000) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Revision for Order #{self.related_order.id}"