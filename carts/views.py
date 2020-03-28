import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View
from django_redis import get_redis_connection

from goods.models import *
from tools.logging_check import logging_check

r = get_redis_connection('carts')
class CartView(View):

    @logging_check
    def get(self,request,username):
        user = request.myuser
        cache_key = 'cart_%s'%(user.id)
        new_all_carts = r.hgetall(cache_key)  # hgetall拿回来的是个字典
        all_carts_sku = SKU.objects.filter(id__in=new_all_carts.keys())
        # filter 查询谓词,查询int型字段,接受字符类型
        # get 查询 查询int型字段,接受字符类型
        # redis返回值中若出现字符类型,均为自节串在结合redids数据进行django orm查询时
        # 查询条件可直接输入,无需转换
        # todo hgetall() 返回值
        skus_list = []
        for cs in all_carts_sku:
            d = {}
            d['id'] = cs.id
            d['name'] = cs.name
            d['price'] = cs.price
            # ImageFiled的值是一个image对象
            d['default_image_url'] = str(cs.default_image_url)
            # {b'1':b'{"count":1,"select":1}'}
            d_j = json.loads(new_all_carts[str(cs.id).encode()])
            d['count'] = d_j['count']
            d['selected'] = d_j['selected']

            # ['尺寸','颜色']
            sku_sale_attr_name = []
            # ['15寸','红色']
            sku_sale_attr_val = []

            sale_attr_vals = SaleAttrValue.objects.filter(sku_id=cs.id)

            for sv in sale_attr_vals:
                sku_sale_attr_val.append(sv.sale_attr_value_name)
                s_name = sv.sale_attr_id.sale_attr_name
                sku_sale_attr_name.append(s_name)
            d['sku_sale_attr_name'] = sku_sale_attr_name
            d['sku_sale_attr_val'] = sku_sale_attr_val
            skus_list.append(d)
        return JsonResponse({'code': 200, 'data': skus_list})

    @logging_check
    def post(self,request,username):
        # 购物车数据  加入到redis  里面有hashmap
        # key ,在hashmap里面filed(sku_id) value(count,选中状态select,)
        # {sku_id:{'count':1,'select':1}}  参照样式
        data = request.body
        json_obj = json.loads(data)
        count = json_obj.get('count')
        sku_id = json_obj.get('sku_id')
        if count:
            count = int(count)
        # 检查 sku_id
        try:
            sku= SKU.objects.get(id = sku_id)
        except Exception as e:
            print('--cart get sku error')
            result = {'code':10301,'error':'Your sku_id is error'}
            return JsonResponse(result)
            # 检查库存和添加数量
        if int(count)>sku.stock:
            result = {'code':10302,'error':'Your count is error'}
            return JsonResponse(result)
        user = request.myuser
        uid = user.id
        # 生成 redis 的存储key
        cache_key = 'cart_%s'%(uid)

        # 第一次存数据

        all_carts = r.hgetall(cache_key)
        if not all_carts:
            # 初始化购物车数据
            # 默认添加购物车时,选中状态为1
            status = {'count':count,'selected':1}
            r.hset(cache_key,sku_id,json.dumps(status))  # 里面应该是json串
        else:
            # redis 有这个用户的购物车数据
            cart_sku = r.hget(cache_key,sku_id)
            if not cart_sku:
                # 第一次存储该sku商品
                status = {'count': count, 'selected': 1}
                r.hset(cache_key, sku_id, json.dumps(status))  # 里面应该是json串
            else:
                # 购物车中有次添加的sku的商品
                cart_sku_data=json.loads(cart_sku)
                old_count = cart_sku_data['count']
                new_count = int(old_count) + int(count)

                #　检查当前购物车该商品的数量已经超过库存
                if new_count > sku.stock:
                    result = {'code': 10302, 'error': 'The count is error'}
                    return JsonResponse(result)
                status = {'count':new_count,'selected':1}
                r.hset(cache_key,sku_id,json.dumps(status))
        # 购物车 redis 数据添加完毕
        # 如何返回 全量or增量
        # {'sku_id':{'count':1,'select':1} }
        new_all_carts = r.hgetall(cache_key)  #hgetall拿回来的是个字典
        all_carts_sku = SKU.objects.filter(id__in=new_all_carts.keys())
        # filter 查询谓词,查询int型字段,接受字符类型
        # get 查询 查询int型字段,接受字符类型
        # redis返回值中若出现字符类型,均为自节串在结合redids数据进行django orm查询时
        # 查询条件可直接输入,无需转换
        # todo hgetall() 返回值
        skus_list = []
        for cs in all_carts_sku:
            d = {}
            d['id']=cs.id
            d['name']=cs.name
            d['price']=cs.price
            # ImageFiled的值是一个image对象
            d['default_image_url']=str(cs.default_image_url)
            # {b'1':b'{"count":1,"select":1}'}
            d_j = json.loads(new_all_carts[str(cs.id).encode()])
            d['count'] = d_j['count']
            d['selected'] = d_j['selected']

            # ['尺寸','颜色']
            sku_sale_attr_name = []
            # ['15寸','红色']
            sku_sale_attr_val = []

            sale_attr_vals = SaleAttrValue.objects.filter(sku_id=cs.id)

            for sv in sale_attr_vals:
                sku_sale_attr_val.append(sv.sale_attr_value_name)
                s_name = sv.sale_attr_id.sale_attr_name
                sku_sale_attr_name.append(s_name)
            d['sku_sale_attr_name']=sku_sale_attr_name
            d['sku_sale_attr_val']=sku_sale_attr_val
            skus_list.append(d)
        return JsonResponse({'code':200,'data':skus_list})








