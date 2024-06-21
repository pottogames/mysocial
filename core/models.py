from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
User = get_user_model()
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

#eliasdaily



class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='media/', null=True)  # Allow null for existing rows
    media_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return f"Story by {self.author.username}"
    
#Elias plugin!
class Plugin(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='plugin_images/')
    file = models.FileField(upload_to='plugin_files/')
    web_link = models.URLField(blank=True, null=True)  # New field for the web link

#trader app!

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField





class UserProfile2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class Interest(models.Model):
    user = models.ForeignKey(User, related_name='interests', on_delete=models.CASCADE)
    category = models.CharField(max_length=100)  # Example field for category


class Artist(models.Model):
    artistName = models.CharField(_("Artist Name"), max_length=50)
    created = models.DateTimeField(_("Artist created date"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Latest artist update"), auto_now=True)

    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")

    def __str__(self):
        return self.artistName

class Album(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, default=None)
    artist = models.ForeignKey(Artist, verbose_name=_("Artist"), on_delete=models.CASCADE, null=True, blank=True)
    albumName = models.CharField(_("Album Name"), max_length=50)
    created = models.DateTimeField(_("Album created date"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Latest album update"), auto_now=True)

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    def __str__(self):
        return self.albumName
    
class Song(models.Model):
    album = models.ForeignKey("Album", verbose_name=_("Song Album"), on_delete=models.CASCADE)
    songThumbnail = models.ImageField(_("Song Thumbnail"), upload_to='thumbnail/', help_text=".jpg, .png, .jpeg, .gif, .svg supported")
    song = models.FileField(_("Song"), upload_to='songs/', help_text=".mp3 supported only",)
    songName = models.CharField(_("Song Name"), max_length=50)
    created = models.DateTimeField(_("Song created date"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Latest song update"), auto_now=True)

    class Meta:
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")

    def __str__(self):
        return self.songName




class Store(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='store_photos/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')

    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    last_activity = models.DateTimeField(default=timezone.now)
    is_sleeping = models.BooleanField(default=False)

    # Add related_name to prevent clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class BanIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255)
    duration = models.DurationField(null=True, blank=True)
    banned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


class Campaign1(models.Model):
    product_link = models.URLField()
    product_name = models.CharField(max_length=255)
    purchase_times = models.IntegerField()
    image = models.ImageField(upload_to='media/image/', default='default.jpg')  # Add this field
    is_queued = models.BooleanField(default=False)
    name = models.CharField(max_length=100, default='Default Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Example default value
    def __str__(self):
        return self.product_name
class Purchase1(models.Model):
    campaign = models.ForeignKey(Campaign1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255)  # PayPal payment ID
    timestamp = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='group_memberships')
    image = models.ImageField(upload_to='group_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Message1(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From: {self.sender} | To: {self.recipient} | Content: {self.content}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uploaded_products = models.ManyToManyField('Product')  # Assuming Product is correctly defined
    




class ReportedMessage(models.Model):
    message = models.ForeignKey('Messages', on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_reason = models.CharField(max_length=255)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reported message {self.message.id}"



class Video(models.Model):
    element_name = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/image/', default='default.jpg')
    video = models.FileField(upload_to='media/video/', default='default_video.mp4')
    likes = models.ManyToManyField(User, related_name='liked_videos', through='Like')
    likes_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)  # Add a share count field with default value 0
    download_count = models.IntegerField(default=0)  # New field for download count
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Recipient(models.Model):
    name = models.CharField(max_length=100)
    # Add any other fields relevant to the Recipient model

class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE) 
    def __str__(self):
        return f'Message by {self.user.username} on {self.video.title}'






class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat Message {self.id} by {self.user.username}'


class FoodItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    image = models.ImageField(upload_to='media/image', null=True, blank=True)

    def __str__(self):
        return self.name

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'user', 'display_image')
    readonly_fields = ('display_image',)  # Make the display_image field read-only

    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 100px;" />')  # Display the image as HTML
        else:
            return None
    display_image.short_description = 'Image Preview'  # Set a short description for the display_image field

# Register the FoodItem model with the admin site using the FoodItemAdmin class
admin.site.register(FoodItem, FoodItemAdmin)



class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='collection_images/', null=True, blank=True)


class WeightTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Specify default value
    bmi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Add BMI field



class Chat2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] 


class Category1(models.Model):
    name = models.CharField(max_length=100)





class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()  # Description field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='product_photos/', null=True, blank=True)
    sku = models.CharField(max_length=50, default='DEFAULT_SKU')
    category = models.ForeignKey(Category1, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    product_link = models.URLField(blank=True, null=True)



class Products(models.Model):
    element_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category1, on_delete=models.CASCADE)  # Update to reference Category1
    video = models.FileField(upload_to='videos/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Button(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have a Product model
    rating = models.IntegerField(default=5)  # Rating from 1 to 5
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
class Post2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drawing_data = models.TextField()  # Store the drawing data as text (base64 encoded)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.user.username}'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=42)  # Ethereum wallet address

    def __str__(self):
        return self.wallet_address

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=100)
    sender = models.CharField(max_length=100, default='default_value')
    timestamp = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'


class ChartData(models.Model):
    symbol = models.CharField(max_length=50)
    date = models.DateField()
    close = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.symbol} - {self.date}"
    
class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.symbol

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
from core.models import Notification

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    notification_type = models.CharField(max_length=100)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')

    def __str__(self):
        return f'{self.user} - {self.notification_type}'
    

class AiChatMessage(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.user_message} | Bot: {self.bot_response}'