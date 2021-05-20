

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

from .models import User,Listing,comments,Bids,Watchlist

from django.db.models import Max

categories_List=["phones & tablets","sports goods","electronic","fashion","home & office","gaming","automobile","sporting-goods"]


def index(request):

    return render(request, "auctions/index.html",{"listings":Listing.objects.filter(status="active"),
    "heading":"Active listings ","count":Listing.objects.filter(status="active").count()
   })
   
def auctions(request):

    
    return render(request, "auctions/index.html",{"listings":Listing.objects.all(),
     "heading":"Auctions","bids":Bids.objects.all(),"count":Listing.objects.all().count()
   })
   

def listing(request,listing_id):
    current_bid=Bids.objects.filter(listing=listing_id).all()
    highest=current_bid.aggregate(Max('Bid'))
    highest_bid=highest.get("Bid__max")
    try:
        listing=Listing.objects.get(id=listing_id)
    
    except Listing.DoesNotExist:
        raise Http404("Sorry,listing does not exist")
       

    som=Bids.objects.get(listing=listing_id,Bid=highest_bid)
    winner=som.user
   

    try:
        listing=Listing.objects.get(id=listing_id)
    
    except Listing.DoesNotExist:
        return HttpResponse("<h1>Sorry,listing does not exist</h1>")
    
    
    first_listing=Bids.objects.filter(listing=listing_id).first()
   
    first_bider=User.objects.get(id=first_listing.user_id)
   

    

   
    if request.method=="POST":
        bid=request.POST["bid"]


   
        
        if int(bid) >  highest_bid:
            new_bid=Bids(Bid=bid,listing=listing,user=request.user)
            new_bid.save()

            listing.price=bid
            listing.save()

            return HttpResponseRedirect(reverse("listing",args=(listing.id,)))

        elif int(bid) <  highest_bid:
            try:
                highest_bider=Bids.objects.get(Bid=highest_bid,listing=listing_id,user=request.user)
            except Bids.DoesNotExist:
                return render(request, "auctions/listing.html",{"listing":Listing.objects.get(pk=listing_id),
    "comments":comments.objects.filter(listing_id=listing_id).all(),
    "bid":highest_bid,"watchlist":Watchlist.objects.filter(user_id=request.user,listing_id=listing_id),"count":current_bid.count(),
    "first_bider":first_bider,"message":f"Bid should be greater that the current bid(${highest_bid})","count":current_bid.count()-1,
   
    })
            return render(request, "auctions/listing.html",{"listing":Listing.objects.get(pk=listing_id),
    "comments":comments.objects.filter(listing_id=listing_id).all(),
    "bid":highest_bid,"watchlist":Watchlist.objects.filter(user_id=request.user,listing_id=listing_id),
    "message":f"Bid should be greater that the current bid(${highest_bid})","count":current_bid.count()-1,
    "highest_bider":Bids.objects.get(Bid=highest_bid,listing=listing_id,user=request.user),
    "first_bider":first_bider
    })

        else:
            try:
                highest_bider=Bids.objects.get(Bid=highest_bid,listing=listing_id,user=request.user)
            except Bids.DoesNotExist:
                return render(request, "auctions/listing.html",{"listing":Listing.objects.get(pk=listing_id),
    "comments":comments.objects.filter(listing_id=listing_id).all(),
    "bid":highest_bid,"watchlist":Watchlist.objects.filter(user_id=request.user,listing_id=listing_id),"count":current_bid.count(),
    "first_bider":first_bider
   
    })

           


    try:
        watchlist=Watchlist.objects.filter(user_id=request.user,listing_id=listing_id)
    except TypeError:
          return render(request, "auctions/listing.html",{"listing":Listing.objects.get(pk=listing_id),
    "comments":comments.objects.filter(listing_id=listing_id).all(),
    "bid":highest_bid,
    "count":current_bid.count()-1,
    })

   

    try:
        highest_bider=Bids.objects.get(Bid=highest_bid,listing=listing_id,user=request.user)
        
    except Bids.DoesNotExist:
        return render(request, "auctions/listing.html",{"listing":Listing.objects.get(pk=listing_id),
    "comments":comments.objects.filter(listing_id=listing_id).all(),
    "bid":highest_bid,"watchlist":Watchlist.objects.filter(user_id=request.user,listing_id=listing_id),
    "message":f"Bid should be greater that the current bid(${highest_bid})","count":current_bid.count()-1,
    "current_user":request.user,"first_bider":first_bider,"winner": winner
   
    })


    

   
    
    return render(request, "auctions/listing.html",{"listing":Listing.objects.get(pk=listing_id),
    "comments":comments.objects.filter(listing_id=listing_id).all(),
    "bid":highest_bid,"watchlist":Watchlist.objects.filter(user_id=request.user,listing_id=listing_id),
    "count":current_bid.count()-1,"highest_bider":Bids.objects.get(Bid=highest_bid,listing=listing_id,user=request.user),
    "current_user":request.user,"first_bider":first_bider,
    "winner": winner
    
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

def category(request,category):
    return render(request, "auctions/category.html",{"listings":Listing.objects.filter(categories=category).all(),"category":category})


def profile(request,username):
    user=User.objects.get(id=username)
    
    return render(request, "auctions/profile.html",{"listings":Listing.objects.filter(user_id=username).all(),
    "username":user.username})

@login_required(login_url='login')
def new(request):
    categories=Listing.objects.values_list('categories',flat=True)
    print(categories)
    
    if request.method=="POST":
        title=request.POST["title"]
        description=request.POST["description"]
        price=request.POST["price"]
        user=request.user
        photo=request.POST["photo"]
       
        category=request.POST["category"]

         # Set timestamp
        myDate = datetime.now()
        formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")

        listing=Listing(title=title,description=description,user_id=user,photo=photo,categories=category,date=formatedDate,price=price)
        listing.save()
        bid=Bids(Bid=price,listing=listing,user=user)
        bid.save()
        return HttpResponseRedirect(reverse("listing",args=(listing.id,)))
        

      
    return render(request, "auctions/new.html",{"categories":categories_List})

@login_required(login_url='login')
def comment(request,listing_id):
    comment=request.POST["comment"]
    user=request.user 
    # Set timestamp
    myDate = datetime.now()
    formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S") 
    listing=Listing.objects.get(pk=listing_id)

    comm=comments(comments=comment,user_id=user,listing_id=listing,date=formatedDate)
    comm.save()
    return HttpResponseRedirect(reverse("listing",args=(listing.id,)))

@login_required(login_url='login')
def add_watchlist(request,listing_id):
    user=request.user
    listing=Listing.objects.get(id=listing_id)
    watchlist=Watchlist(user_id=user,listing_id=listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("listing",args=(listing.id,)))

@login_required(login_url='login')
def remove_watchlist(request,listing_id):
    
    listing=Listing.objects.get(id=listing_id)
    watchlist=Watchlist.objects.filter(listing_id=listing,user_id=request.user)
    watchlist.delete()
    return HttpResponseRedirect(reverse("listing",args=(listing.id,)))

@login_required(login_url='login')
def watchlist(request):
    watchlist=Watchlist.objects.filter(user_id=request.user).all()
  
    
    
  
    return render(request, "auctions/watchlist.html",{"contents":watchlist})

@login_required
def close_auction(request,listing_id):
    listing=Listing.objects.get(id=listing_id)
    listing.status="closed"
    listing.save()

    
    return HttpResponseRedirect(reverse("listing",args=(listing.id,)))

    
    

   
