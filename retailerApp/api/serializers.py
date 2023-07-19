from rest_framework import serializers
from retailerApp.models import *
from wholesellerApp.models import Wholeseller
from wholesellerApp.api.serializers import WholesellerSerializer
from productApp.api.serializers import FilterListSerializer
from drf_extra_fields.fields import Base64ImageField

class RetailerNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerMobile
        fields = '__all__'

class RetailerSerializer(serializers.ModelSerializer):
    wholeseller_details = serializers.SerializerMethodField()
    retailer_image = Base64ImageField(required=False)
    retailer_adhar_front_image = Base64ImageField(required=False)
    retailer_adhar_back_image = Base64ImageField(required=False)
    retailer_pancard_image = Base64ImageField(required=False)
    retailer_gst_image = Base64ImageField(required=False)
    retailer_number = RetailerNumberSerializer(many = True)
    class Meta:
        model = Retailer
        fields = '__all__'

    def get_wholeseller_details(self, obj):
        wholesellers = obj.retailer_wholeseller.all().order_by("id")
        wholeseller_data = WholesellerSerializer(wholesellers, many=True).data
        return wholeseller_data

    def update(self, instance, validated_data):
        instance.retailer_image = validated_data.get(
            'retailer_image')
        instance.retailer_adhar_front_image = validated_data.get(
            'retailer_adhar_front_image')
        instance.retailer_adhar_back_image = validated_data.get(
            'retailer_adhar_back_image')
        instance.retailer_pancard_image = validated_data.get(
            'retailer_pancard_image')
        event = super().update(instance, validated_data)
        return event

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


# -----------------------wholeseller retailer-----------------------

class WholesellerRetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = '__all__'
