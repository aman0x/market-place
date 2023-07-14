from rest_framework import serializers
from retailerApp.models import *
from wholesellerApp.models import Wholeseller
from wholesellerApp.api.serializers import WholesellerSerializer
from productApp.api.serializers import FilterListSerializer


class RetailerSerializer(serializers.ModelSerializer):
    wholeseller_details = serializers.SerializerMethodField()
    class Meta:
        model = Retailer
        fields = '__all__'

    def get_wholeseller_details(self, obj):
        wholesellers = obj.retailer_wholeseller.all().order_by("id")
        wholeseller_data = WholesellerSerializer(wholesellers, many=True).data
        return wholeseller_data


class CartSerializer(serializers.ModelSerializer):
    product_price_per_qty = serializers.SerializerMethodField()
    total_per_product = serializers.SerializerMethodField()
    class Meta:
        model = SubCart
        fields = '__all__'

    def get_product_price_per_qty(self, obj):
        product_id = obj.product_id
        product = Product.objects.filter(id=product_id)
        product_details = FilterListSerializer(product, many=True).data
        product_price = product_details[0]['product_selling_price']
        return product_price

    def get_total_per_product(self, obj):
        product_price = self.get_product_price_per_qty(obj)
        qty = obj.qty
        total = product_price * qty
        return total


class CheckoutSerializer(serializers.ModelSerializer):
    cart_details = serializers.SerializerMethodField()
    total_per_cart = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = '__all__'

    def get_cart_details(self, obj):
        cart = obj.cart.all().order_by("id")
        cart_details = CartSerializer(cart, many=True).data
        return cart_details

    def get_total_per_cart(self, obj):
        cart = obj.cart.all().order_by("id")
        total_per_cart = 0
        for cart_item in cart:
            product_price = cart_item.product.product_selling_price
            qty = cart_item.qty
            total_per_cart += product_price * qty
        return total_per_cart
