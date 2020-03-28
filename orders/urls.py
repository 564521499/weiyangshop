from django.conf.urls import url
from . import views
urlpatterns = [
# http://127.0.0.1:8000/v1/orders/processing/?status=1&order_status=0
    url(r'^/processing/$',views.OrderProcessView.as_view())
]