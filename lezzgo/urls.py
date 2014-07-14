from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lezzgo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'lezzdrive.views.home', name='home'),
    url(r'^profile/$', 'lezzdrive.views.profile', name='profile'),


    # Register/Log In
    url(r'^register/$', 'lezzdrive.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    # Find/Offer Rides
    url(r'^find_ride/$', 'lezzdrive.views.find_ride', name='find_ride'),
    url(r'^no_matching_rides/$', 'lezzdrive.views.no_matching_rides', name='no_matching_rides'),
    url(r'^choose_ride/$', 'lezzdrive.views.choose_ride', name='choose_ride'),
    url(r'^confirm_ride/(?P<ride_id>\w+)/$', 'lezzdrive.views.confirm_ride', name='confirm_ride'),
    url(r'^offer_ride/$', 'lezzdrive.views.offer_ride', name='offer_ride'),
    url(r'^publish_ride/(?P<ride_id>\w+)/$', 'lezzdrive.views.publish_ride', name='publish_ride'),
    url(r'^cancel_seat/(?P<ride_id>\w+)/$', 'lezzdrive.views.cancel_seat', name='cancel_seat'),

     # Profile pages
    url(r'^profile/ride-information/$', 'lezzdrive.views.rides', name='rides'),
    url(r'^profile/account-settings/$', 'lezzdrive.views.account', name='account'),
    url(r'^profile/welcome/$', 'lezzdrive.views.welcome', name='welcome'),

    # Reset Password
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # Support old style base36 password reset links; remove in Django 1.7
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm_uidb36'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    url(r'^admin/', include(admin.site.urls)),

    # Twilio URLs
    # url(r'^sms/$', 'lezzdrive.views.sms', name='sms'),
    # url(r'^ring/$', 'lezzdrive.views.ring'),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)