# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
# ...

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    from django.db import IntegrityError
    from django.contrib.auth.password_validation import validate_password
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email

    if request.method != "POST":
        return JsonResponse({"error": "Use POST to register."}, status=405)

    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({"error": "Expected a JSON object."}, status=400)

    fields = ["userName", "password", "email", "firstName", "lastName"]
    if any(not isinstance(data.get(field, ""), str) for field in fields):
        return JsonResponse({"error": "Fields must contain text."}, status=400)

    username = data.get("userName", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()
    first_name = data.get("firstName", "").strip()
    last_name = data.get("lastName", "").strip()

    if not username or not password or not email:
        return JsonResponse(
            {"error": "Username, password, and email are required."},
            status=400,
        )

    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    try:
        user.full_clean(exclude=["password"])
        validate_email(email)
        validate_password(password, user=user)
    except ValidationError as error:
        return JsonResponse(
            {"error": " ".join(error.messages)},
            status=400,
        )

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
    except IntegrityError:
        return JsonResponse(
            {"error": "That username is already taken."},
            status=400,
        )

    login(request, user)
    return JsonResponse({
        "userName": user.username,
        "status": "Authenticated",
    })


def get_cars(request):
    from .models import CarMake, CarModel
    from .populate import initiate

    if not CarMake.objects.exists():
        initiate()

    car_models = CarModel.objects.select_related("car_make").order_by("id")
    cars = [
        {"CarModel": model.name, "CarMake": model.car_make.name}
        for model in car_models
    ]
    return JsonResponse({"CarModels": cars})
