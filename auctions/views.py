from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import * 


def index(request):
     return render(request, "auctions/index.html", {
                "listing": AuctListing.objects.all()
            })
@login_required(login_url='login')
def product(request, product_title):
    if request.method == "POST":
        if request.POST.get("new_bid"):
            toCompare = AuctListing.objects.get(title=product_title)
            new_Bid = int(request.POST["new_bid"])
            entry = AuctListing.objects.get(title=product_title)
            entry.starting_bid = new_Bid
            entry.save()
            return render(request, "auctions/product.html", {
                "product_name": entry,
                "toCompare": toCompare
            })

        else:
            if request.POST.get("delete_field"):
                print("OPAAAAAAAAAA")
                user_logged = request.user.get_username()
                toShow = AuctListing.objects.get(title=product_title)
                toCompare = AuctListing.objects.get(title=product_title)
                user_created = toShow.user_name
                if user_logged == user_created:
                    toCompare.delete()
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "auctions/product.html", {
                        "product_name": toShow
                    })
            else:
                comment = str(request.POST.get("comments_add"))
                comentario_criar = commentsListing(comments= comment)
                comentario_criar.save()
                comment_add_auct = AuctListing.objects.get(title=product_title)
                comment_add_auct.comments_title.add(comentario_criar)
                all_comments = comment_add_auct.comments_title.all()
                toCompare = AuctListing.objects.get(title=product_title)
                return render(request, "auctions/product.html", {
                    "product_name": comment_add_auct,
                    "comments": all_comments,
                    "toCompare": toCompare,
                })


    else:
        print("AKIIIIIIIIII")
        comment_add_auct = AuctListing.objects.get(title=product_title)
        all_comments = comment_add_auct.comments_title.all()
        user_logged = request.user.get_username()
        toShow = AuctListing.objects.get(title=product_title)
        toCompare = AuctListing.objects.get(title=product_title)
        user_created = toShow.user_name
        if user_logged == user_created:
            return render(request, "auctions/product.html", {
                "product_name": toShow,
                "toCompare": toCompare,
                "comments": all_comments
            })
        else:
            return render(request, "auctions/product.html", {
                "product_name": toShow
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

@login_required(login_url='login')
def create_listing(request):
    if request.method == "GET":
            return render(request, "auctions/create_listing.html", {
                "listing": AuctListing.objects.all()
            })
    else:
        userName = request.user.get_username()
        title_to_add = str(request.POST["title_form"])
        description_to_add = str(request.POST["description_form"])
        bid_to_add = int(request.POST["starting_Bid"])
        auctListing = AuctListing(title= title_to_add, description= description_to_add, starting_bid= bid_to_add, user_name= userName)
        auctListing.save()

        return HttpResponseRedirect(reverse("create"))

