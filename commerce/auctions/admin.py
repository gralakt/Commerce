from django.contrib import admin

# Register your models here.
from .models import User, Bid, Category, Listing, Comment
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)