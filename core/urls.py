from django.urls import path
from . import views
from django.urls import path
from .views import ProductListView, ProductDetailView
from .views import dashboard,edit_product
from .views import process_payment, payment_successful, payment_failed
from .views import delete_message
from .views import group_list
from .views import views_404
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.submit_form, name='submit_form1'),  # Ensure this line matches your view function
    path('signup/', views.submit_form, name='submit_form2'),  # Ensure this line matches your view function
    #eliasDAILY
    path('create-story/', views.upload_story, name='create_story'),
    path('api/stories/', views.stories_api, name='stories_api'),
    path('eliasdaily/', views.Eliasdaily, name='Eliasdaily'), 
    path('signup/', views.submit_form, name='submit_form'),  # Ensure this line matches your view function
    path('signin/', views.rectap, name='rectap'),  # Ensure this line matches your view function
    path('api/chat/', views.chat_view, name='chat_view'),
    #plugin app
    path('plugin/app', views.plugin_list, name='plugin_list'),
    path('plugin/<int:plugin_id>/details/', views.plugin_details, name='plugin_details'),
    #trading app
    path('save/', views.save_changes, name='save_changes'),
    path('delete/', views.delete_changes, name='delete_changes'),
    path('connect_wallet/', views.connect_wallet, name='connect_wallet'),
    path('disconnect_wallet/', views.disconnect_wallet, name='disconnect_wallet'),
    path('view_wallet_balance/', views.view_wallet_balance, name='view_wallet_balance'),
    path('trade/api/stocks/', views.stock_chart, name='get_stock_symbols'),
    path('trade/api/stocks/<str:symbol>/', views.get_stock_chart_data, name='get_stock_chart'),
    path('presentation_videos/<int:video_id>/', views.presentation_videos, name='video_presentation'),
    path('elias/trade/', views.tradeindex, name='viral'),
    path('chart/<str:symbol>/', views.stock_chart, name='stock_chart'),
    path('viral/', views.viral, name='viral'),
    path('searchgo/', views.gosearch, name='go'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/submit_review/', views.submit_review, name='submit_review'),
    # Add other URLs
    path('index/<uuid:pk>/', views.post_detail, name='post_detail'),
    path('music/create/',views.upload_song, name="upload_song"),
    path('music/index/', views.indexs, name="index"),
    path('music/search/', views.search_songs, name='search_songs'),
    path('paint/create_post', views.create_post, name="create"),
    path('help/', views.help, name='help'),
    path('about/', views.about, name='about'),
    path('camera/', views.camera, name='camera'),
    path('explain/', views.explain, name='explain'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('download/', views.download, name="download"),
    path('campign_start/', views.create_campaign, name='campign_start'),
    path('campaign_detail/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('pay/<int:pk>/', views.pay, name='pay'),
    path('purchase_success/', views.paypal_payment, name='purchase_success'),
   # path('error1/', views.error1, name='error1'),
    #path('queue/', views.queue_campaign, name='queue'),
    #path('checkout/<int:campaign_id>/', views.checkout, name='checkout'),
   # path('waiting/<int:campaign_id>/', views.waiting, name='waiting'),
   # path('start_campign/<int:store_id>/', views.upload_image, name='upload_image'),
    path('drow/', views.create_post, name='create_post'),    
    path('food/home/', views.home_food, name="food_home"),
    path('stores/search/', views.search_stores, name='search_stores'),  # URL pattern for searching stores
    path('products/store_list/', views.stores_list, name='store_list'),
    path('upload_product/<int:store_id>/', views.upload_product, name='upload_product'),
    path('create_store/', views.create_store, name='create_store'),
    path('edit_store/<int:store_id>/', views.store_edit, name='edit_store'),
    path('store_detail/<int:store_id>/', views.stores, name='store_detail'),
    path('store_products/<int:store_id>/', views.store_products, name='store_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('report_message/<int:message_id>/', views.report_message, name='report_message'),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('video_messages/<int:video_id>/', views.video_messages, name='video_messages'),
    path('earn/', views.earn, name='earn'),
    path('group/<int:group_id>/send_message/', views.send_group_message, name='send_group_message'),
    path('products/category/<int:category_id>/', views.all_products, name='product_list_by_category'),
    path('like_video/<int:video_id>/', views.like_video, name='like_video'),
    path('search1/', views.search1, name='search1'),
    path('search_results/', views.search_results, name='search_results'),
    path('all_messages/', views.all_messages, name='all_messages'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('join-group/<int:group_id>/', views.join_group, name='join_group'),
    path('leave-group/<int:group_id>/', views.leave_group, name='leave_group'),
    path('group-list/', views.group_list, name='group_list'),
    path('create_group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_chat, name='group_chat'),
    path('send_private_message/<int:recipient_id>/', views.send_private_message, name='send_private_message'),
    path('chat/', views.chat, name="chat"),
    path('home_ai/', views.home_ai, name="home_ai"),
    path('genarante_photo/', views.genarante_photo, name="genarante_photo"),
    path("chat/<slug:conversation_id>/", views.chat, name="chat_with_id"),
    path('delete_message/', delete_message, name='delete_message'),
    path('presentation/', views.presentation_videos, name='presentation_videos'),
    path('create_video/', views.create_video, name='create_video'),
    path('change_category/<int:category_id>/', views.change_category, name='change_category'),
    path('change_category/', views.change_category, name='change_category'),
    path('view-food-items/', views.view_food_items, name='view_food_items'),   
    path('track-weight/', views.track_weight, name='track_weight'),
    path('chat_about_food/', views.chat2, name='chat2'),
    path('products/<int:pk>/update/', views.edit_product, name='update_product'),
    path('get_product_details/', views.get_product_details, name='get_product_details'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('process_payment/<int:store_id>/', views.process_payment, name='process_payment'),
    path('payment_successful/', views.payment_successful, name='payment_successful'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('dashboard_start/', views.dashboard, name='dashboard_start'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('all/', views.all_products, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/detail/', views.cart_detail, name='cart_detail'),
    path('products/<int:product_id>/<int:pk>/', views.product_detail, name='product_detail'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('upload/mobile/', views.uploadm, name='uploadm'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]

handler404 = views_404