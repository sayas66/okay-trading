from commerce.views import SignUpView, SignOutView, SignInView

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^account/sign-in/$', SignInView.as_view(), name='sign_in'),
    url(r'^account/sign-up/$', SignUpView.as_view(), name='sign_up'),
    url(r'^account/sign-out/$', SignOutView.as_view(), name='sign_out'),
    
    url(r'', include('commerce.urls', namespace='commerce', app_name='commerce')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
