from django.db import models

# Create your models here.
from goods.models import SKU
from user.models import *

ORDER_STATUS = (
    (1, '待付款'), (2, '待发货'), (3, '待收货'), (4, '订单完成')
)


class OrderInfo(models.Model):
    # 订单表
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name='订单编号')
    user = models.ForeignKey(UserProfile)
    address = models.ForeignKey(Address)
    total_count = models.IntegerField(default=1, verbose_name='订单总数')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    freight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    status = models.SmallIntegerField(verbose_name='订单状态', choices=ORDER_STATUS)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'
        verbose_name = '订单基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s_%s_%s' % (self.order_id, self.user.username, self.status)


class OrderGoods(models.Model):
    order = models.ForeignKey(OrderInfo)
    sku = models.ForeignKey(SKU)
    count = models.IntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')

    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name
