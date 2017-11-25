from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', 'commerce.views.splash', name='splash'),
    url(r'^home$', 'commerce.views.index', name='index'),
    # url(r'^$', 'commerce.views.index', name='index'),
    url(r'^information/$', 'commerce.views.information', name='information'),    
    url(r'^condition/$', 'commerce.views.condition', name='condition'),    
    
    url(r'^category/$', 'commerce.views.display_category_random', name='display_category_random'),
    url(r'^category/(?P<category_id>\d+)/$', 'commerce.views.display_category', name='display_category'),
    url(r'^product-min-price/$', 'commerce.views.display_product_min_price', name='display_product_min_price'),
    url(r'^product-min-moq/$', 'commerce.views.display_product_min_moq', name='display_product_min_moq'),
    url(r'^product/(?P<product_id>\d+)/$', 'commerce.views.display_product', name='display_product'),
    
    url(r'^account/profile/$', 'commerce.views.account', name='account'),
    url(r'^order/$', 'commerce.views.display_order', name='display_order'),
    url(r'^add-address/$', 'commerce.views.add_address', name='add_address'),
    url(r'^addresses/$', 'commerce.views.addresses', name='addresses'),
    url(r'^remove-addresses/(?P<address_id>\d+)/$', 'commerce.views.remove_address', name='remove_address'),
    
    url(r'^cart/(?P<product_id>\d+)/(?P<qty>\d+)/$', 'commerce.views.add_to_cart', name='cart'),
#     url(r'^remove-from-cart/(?P<product_id>\d+)/$', 'commerce.views.remove_from_cart', name='remove_from_cart'),
    url(r'^shipping/(?P<product_id>\d+)/$', 'commerce.views.shipping', name='shipping'),
    
    url(r'^shipping-special/$', 'commerce.views.shipping_special', name='shipping_special'),
    
    url(r'print-contrat/(?P<order_id>\d+)/$', 'commerce.views.print_contrat', name='print_contrat'),
    
    url(r'^display-users/$', 'commerce.views.display_users', name='display_users'),
    url(r'^display-user-order/(?P<id>\d+)/$', 'commerce.views.display_users_order', name='display_users_order'),
    url(r'^display-users-order/special/$', 'commerce.views.display_users_order_special', name='display_users_order_special'),
    url(r'^display-user-order/special/validate/(?P<id>\d+)/$', 'commerce.views.users_order_special_validate', name='users_order_special_validate'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
