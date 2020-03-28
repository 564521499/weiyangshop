from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^/index$',views.GoodsIndexView.as_view()),

    #http://127.0.0.1:8000/v1/goods/catalogs/1?launched=true&page=1
    url(r'^/catalogs/(?P<catalog_id>\d+)$',views.GoodsListView.as_view()),


    url(r'^/detail/(?P<sku_id>\d+)/$',views.GoodsDetailView.as_view()),
]