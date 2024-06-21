from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount
from .models import Product
from .models import Chat
from .models import Video, Category
from .models import ChatMessage
from .models import Group, GroupMessage
from .models import Category1
from .models import Collection
from .models import Like,Messages
from .models import Campaign1, Purchase1,Review
from django.utils.html import format_html
from .models import BanIP
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Notification
from .models import Store
from .models import Story,AiChatMessage
admin.site.register(AiChatMessage)
admin.site.register(Story)
admin.site.register(ChatMessage)
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Product)
admin.site.register(Chat)
admin.site.register(Video)
admin.site.register(Category)
admin.site.register(Group)
admin.site.register(GroupMessage)
admin.site.register(Category1)
admin.site.register(Collection)
admin.site.register(Like)
admin.site.register(Messages)
admin.site.register(Notification)
admin.site.register(Store)



@admin.register(Campaign1)
class Campaign1Admin(admin.ModelAdmin):
    list_display = ('id', 'product_link', 'product_name', 'purchase_times', 'image_preview', 'is_queued')
    list_filter = ('is_queued',)
    search_fields = ('product_name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;">', obj.image.url)
        else:
            return 'No Image'

    image_preview.short_description = 'Image Preview'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # If it's a new campaign, set the creator to the current user
            obj.creator = request.user

        # Check if the user is an admin before allowing the change of image
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        else:
            # If user is not an admin, only save the model without changing the image
            obj.save(update_fields=['product_link', 'product_name', 'purchase_times', 'is_queued'])

@admin.register(Purchase1)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'campaign', 'user', 'quantity', 'total_amount', 'payment_id', 'timestamp')


@admin.register(BanIP)
class BanIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'duration', 'banned_at')
    search_fields = ('ip_address', 'reason')
    actions = ['unban_ip']

    def unban_ip(self, request, queryset):
        queryset.delete()
    unban_ip.short_description = 'Unban selected IP addresses'

from .models import UserProfile2

class UserProfile2Admin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']

admin.site.register(UserProfile2, UserProfile2Admin)

from .models import Song, Album, Artist

# Custom admin class for Song model
class SongAdmin(admin.ModelAdmin):
    list_display = ('songName', 'album', 'created', 'last_updated')  # Display these fields in the list view

# Custom admin class for Album model
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('albumName', 'get_artist_name', 'created', 'last_updated')  # Display these fields in the list view

    def get_artist_name(self, obj):
        return obj.artist.artistName if obj.artist else None

    get_artist_name.short_description = 'Artist'  # Set the column header name
from .models import Plugin


class PluginAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_image_url', 'get_web_link')

    def get_image_url(self, obj):
        return obj.image.url if obj.image else ''

    def get_web_link(self, obj):
        # Assuming you have a 'web_link' field in your Plugin model
        return obj.web_link if obj.web_link else ''

    get_image_url.short_description = 'Image URL'
    get_web_link.short_description = 'Web Link'

admin.site.register(Plugin, PluginAdmin)

# Custom admin class for Artist model
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artistName', 'created', 'last_updated')  # Display these fields in the list view

# Register your models with custom admin classes
admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating']
    list_filter = ['product', 'rating']


#trader app 
