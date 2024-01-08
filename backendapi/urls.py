from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from adsapi.views import AddtoWishListItemsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
    path('api/contactus/',include('pagesapi.urls')),
    path('api/adsapi/',include('adsapi.urls')),
    path('api/blogsapi/',include('blogsapi.urls')),
    path('api/profileapi/',include('profileapi.urls')),
    # path('api/openMoney/',include('opneMoney.urls')),
    #Social oauth URLS
    #Phone Login
    path('api/phone/',include('otp_reg.urls')),
    #WishList URLS
    path('addwishlistitems/<int:pk>', AddtoWishListItemsView.as_view(),name='add-to-wishlist'),
    #AdsComments URLS
    path('api/comment/',include('commentbox.urls')),
    #BlogsComments URLS
    path('api/blogscomment/',include('blogscommentbox.urls')),
    #Payment API
    path('api/payment/',include('paymentapi.urls')),
    # path('api/payu/', include('payu_app.urls')),
    

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
