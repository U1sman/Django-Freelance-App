from django.urls import path
from .api import users, gigs, orders

urlpatterns = [
# Users
    path("signup/", users.signup, name="signup"),
    path("login/", users.login, name="login"),
    path("user/<str:user_id>/", users.get_user, name="get_user"),
    path("check_authenticated_status/", users.check_authenticated_status, name="check_authenticated_status"),

# Gigs
    path("get_gigs/", gigs.get_gigs, name="get_gigs"),
    path("get_all_categories/", gigs.get_all_categories, name="get_all_categories"),
    path("get_categoryGigs/<str:category_name>/", gigs.get_categoryGigs, name="get_categoryGigs"),
    path("get_gig/<str:gig_id>/", gigs.get_gig, name="get_gig"),
    path("get_gig_reviews/<str:gig_id>/", gigs.get_gig_reviews, name="get_gig_reviews"),


# Orders
    path("create_order/", orders.create_order, name="create_order"),
    path("get_order/<str:order_id>/", orders.get_order, name="get_order"),
    path("get_all_order_deliveries/<str:order_id>/", orders.get_all_order_deliveries, name="get_all_order_deliveries"),
    
]
