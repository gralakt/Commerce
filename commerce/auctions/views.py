from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm
from django.contrib import messages

def index(request):
    q = request.GET.get("q") if request.GET.get("q") != None else''
    listings = Listing.objects.filter(category__name__icontains=q, status='active')
    topics = Category.objects.all()
    user = request.user
    context = {'listings': listings, 'topics': topics, 'user': user, 'query': q}
    return render(request, "auctions/index.html", context)


def createListing(request):
    form = ListingForm()

    if request.method == 'POST':

        form = ListingForm(request.POST, request.FILES)

        if form.is_valid():

            filled_form = form.save(commit=False)
            print(filled_form.picture)
            new_bid = Bid.objects.create(
                user = request.user,
                bid = request.POST.get('number'))

            new_listing = Listing.objects.create(
                picture = filled_form.picture,
                title = filled_form.title,
                description = filled_form.description,
                user = request.user,
                bid = new_bid,
                category = filled_form.category,
                status = 'active'

                )

            
                
            return redirect('index')
    context = {'form': form}
    return render(request, "auctions/create.html", context)



def detail(request, pk):
    listing = Listing.objects.get(id=pk)
    user = request.user
    comments = listing.comment_set.all()
    if user.is_authenticated:
        watchlist = user.followers.all()
    else:
        watchlist = None
    if request.method == 'POST':
        if request.POST.get('content') is not None:
            comment = Comment.objects.create(
                user = request.user,
                listing = listing,
                content = request.POST.get('content')
                )
            return redirect('detail', pk=listing.id)

        elif request.POST.get('number') is not None:
            new_bid = Bid.objects.create(
                user = request.user,
                bid = request.POST.get('number'))
            if int(listing.bid.bid) < int(new_bid.bid):
                listing.bid = new_bid
                listing.save()
            else:
                messages.error(request, 'Your bid must be higher than the current bid')
                return redirect('detail', pk=listing.id)
        elif request.POST.get('close-button') is not None:
            listing.status = "disactive"
            listing.save()    
            return redirect('detail', pk=listing.id)

        elif request.POST.get('remove-button') is not None:
            user.followers.remove(listing)
            return redirect('detail', pk=listing.id)

        else:
            user.followers.add(listing)
            return redirect('detail', pk=listing.id)


    context = {'listing': listing, 'comments': comments, 'user': user, 'watchlist': watchlist}

    return render(request, "auctions/detail.html", context)


def watchlist(request, pk):
    user = User.objects.get(id=pk)
    listings = user.followers.all()
    user.followers.add()

    context = {'listings': listings, 'user': user}
    return render(request, "auctions/watchlist.html", context)





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
