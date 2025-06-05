from django.urls import path
from . import views

urlpatterns = [
    # POST
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),

    # GET
    path("user/<int:user_id>/", views.get_user, name="get_user"),
    path("get_all_gigs/", views.get_all_gigs, name="get_all_gigs"),
    path("check_authenticated_status/", views.check_authenticated_status, name="check_authenticated_status"),
    path("get_all_categories/", views.get_all_categories, name="get_all_categories"),
    path("get_categoryGigs/<str:category_name>/", views.get_categoryGigs, name="get_categoryGigs"),
    path("get_gig/<int:gig_id>/", views.get_gig, name="get_gig"),


]
