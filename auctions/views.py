from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, DatabaseError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not username or not email or not password or not confirmation:
            return render(request, "auctions/register.html", {
                "message": "No field can be Empty."
            })
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        bid = request.POST["bid"]
        description = request.POST["description"]
        image_url = request.POST["image"]
        category = request.POST["category"]
        DEFAULT_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdD7G7FFg1UKZFXhyP45b4AvY-qKEFvfjj3w&s"

        if image_url == "":
            image_url = DEFAULT_IMAGE

        if not title or not bid or not description:
            return render(request, "auctions/listing.html", {
                "message": "Fill the required fields"
            })
        try:
            listing = Listing.objects.create(
                title=title,
                owner=request.user,
                starting_bid=bid,
                description=description,
                image=image_url,
                category=category
            )
            listing.save()
            return redirect("index")
            
        except DatabaseError:
            return render(request, "auctions/listing.html", {
                "message": "Something went wrong. Try again"
            })

    else:
        return render(request, "auctions/listing.html")
    

@login_required
def profile(request):
    listings = Listing.objects.filter(owner=request.user)
    total_bids_won = Listing.objects.filter(winner=request.user.username, is_active=False).count()
    return render(request, "auctions/profile.html", {
        "listings": listings,
        "total_listings": listings.count(),
        "total_bids_won": total_bids_won
    })


@login_required
def watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    listings = Listing.objects.filter(id__in=watchlists.values_list("item_id", flat=True))
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def product(request, product_id):
    listing = Listing.objects.get(id=product_id)
    bids = Bid.objects.filter(item=product_id)
    highest_bid = bids.order_by("-bid").first()
    comments = Comment.objects.filter(item=product_id).order_by("-added_at")
    in_watchlist = None
    
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(user=request.user, item=listing).exists()
    else:
        in_watchlist = False
    if request.method == "POST":
        response = request.POST['action']
        if response == 'toggle_watchlist':
            item = Watchlist.objects.filter(user=request.user, item=listing)
            if item.exists():
                item.delete()
            else:
                Watchlist.objects.create(user=request.user, item=listing)
            return redirect('product', product_id)
        
        if response == "place_bid":
            bid = int(request.POST["bid"])
            if highest_bid is None:
                if bid < listing.starting_bid:
                    messages.error(request, "Your bid amount should be higher than current bid.")
                    return redirect('product', product_id)
            elif bid < highest_bid.bid:
                messages.error(request, "Your bid amount should be higher than current bid.")
                return redirect('product', product_id)
            
            Bid.objects.create(user=request.user, item=listing, bid=bid)
            return redirect('product', product_id)
        
        if response == "close_auction":
            listing.is_active = False
            listing.save()
            return redirect('product', product_id)
        
        if response == "user_comment":
            comment = request.POST["user_comment"].strip()
            if comment:
                try:
                    Comment.objects.create(item=listing, user=request.user, comment=comment)
                    return redirect("product", product_id)
                except DatabaseError as e:
                    print("Error when inserting comment: ", e)
                    pass
            else:
                return redirect("product", product_id)

    else:
        return render(request, "auctions/product.html", {
            "listing": listing,
            "bids": bids,
            "highest_bid": highest_bid,
            "in_watchlist": in_watchlist,
            "comments": comments
        })


def category(request):
    categories = Listing.objects.filter(is_active=True).values("category").annotate(count=Count("id"))
    for category in categories:
        print(category['category'])
    return render(request, "auctions/category.html", {
        "categories": categories
    })


def specific_category(request, category_name):
    listings = Listing.objects.filter(category=category_name, is_active=True)
    return render(request, "auctions/specific_category.html", {
        "listings": listings,
        "category_name": category_name
    })