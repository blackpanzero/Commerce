from django.contrib import admin

# Register your models here.
from .models import Listing,comments,Bids,Watchlist,User

class ListingAdmim(admin.ModelAdmin):
    list_display=("id","title","photo","date","user_id")

admin.site.register(Listing)
admin.site.register(comments)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(User)