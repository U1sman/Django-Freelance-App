from django.urls import path
from .api import users, gigs, orders

urlpatterns = [
    # Users
    path("auth/signup/", users.signup, name="signup"),
    path("auth/login/", users.login, name="login"),
    path("auth/status/", users.check_authenticated_status, name="check_authenticated_status"),
    path("users/<str:user_id>/", users.get_user, name="get_user"),

    # Gigs
    path("gigs/", gigs.get_gigs, name="get_gigs"),
    path("gigs/categories/", gigs.get_all_categories, name="get_all_categories"),
    path("gigs/create/", gigs.create_gig_and_pricing_plan, name="create_gig_and_pricing_plan"),
    path("gigs/reviews/create/", gigs.create_gig_review, name="create_gig_review"),
    path("gigs/<str:gig_id>/", gigs.get_gig, name="get_gig"),
    path("gigs/<str:gig_id>/reviews/", gigs.get_gig_reviews, name="get_gig_reviews"),

    # Orders
    path("orders/", orders.get_orders, name="get_orders"),
    path("orders/create/", orders.create_order, name="create_order"),
    path("orders/activity/create/", orders.create_order_activity, name="create_order_activity"),
    path("orders/delivery/create/", orders.create_order_delivery, name="create_order_delivery"),
    path("orders/revision/create/", orders.create_revision_request, name="create_revision_request"),
    path("orders/<str:order_id>/", orders.get_order, name="get_order"),
    path("orders/<str:order_id>/requirements/", orders.get_order_requirements, name="get_order_requirements"),
    path("orders/<str:order_id>/deliveries/", orders.get_order_deliveries, name="get_order_deliveries"),
    path("orders/<str:order_id>/activities/", orders.get_order_activities, name="get_order_activities"),
    path("pricingoptions/<str:order_id>/details/", orders.get_pricing_option_details, name="get_pricing_option_details"),


]
