from rest_framework import serializers
from retailerApp.models import *
from wholesellerApp.models import Wholeseller, Offers
from wholesellerApp.api.serializers import WholesellerSerializer
from productApp.api.serializers import ProductSerializer
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Sum, Min


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
    retailer_number_and_details = serializers.SerializerMethodField()

    class Meta:
        model = Retailer
        fields = '__all__'

    def get_wholeseller_details(self, obj):
        wholesellers = obj.retailer_wholeseller.all().order_by("id")
        wholeseller_data = WholesellerSerializer(wholesellers, many=True).data
        return wholeseller_data

    def get_retailer_number_and_details(self, obj):
        retailer_number = obj.retailer_number.all().order_by('id')
        retailer_numb = RetailerNumberSerializer(retailer_number, many=True).data
        return retailer_numb

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


class SubCartSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = SubCart
        fields = "__all__"

    def get_total_price(self, obj):
        if obj.product:
            total_price = obj.qty * obj.product.product_selling_price

            # Check if the product has any offers
            product_offers = Offers.objects.filter(product=obj.product)

            if product_offers.exists():
                # Select the lowest offer price
                lowest_offer_price = product_offers.aggregate(Min('offer_discounted_price'))['offer_discounted_price__min']
                if lowest_offer_price:
                    lowest_offer_price = int(lowest_offer_price)  # Convert to integer
                    total_price = min(total_price, obj.qty * lowest_offer_price)

            return total_price
        return 0

    def get_product_details(self, obj):
        return obj.product


class CartSerializer(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    cart_product_details = SubCartSerializer(source='cart_items', read_only=True, many=True)

    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_value(self, obj):
        total = 0
        for cart_item in obj.cart_items.all():
            total += cart_item.qty * cart_item.product.product_selling_price
        return total

    def get_total_items(self, obj):
        return obj.cart_items.aggregate(Sum('qty'))['qty__sum'] or 0


class MyPerformanceOrder(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    cart_items = SubCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_value(self, obj):
        total = 0
        for cart_item in obj.cart_items.all():
            total += cart_item.qty * cart_item.product.product_selling_price
        return total

    def get_total_items(self, obj):
        return obj.cart_items.aggregate(Sum('qty'))['qty__sum'] or 0

    def get_cart_items(self, obj):
        return obj.cart_items

class CartDetailedSerializer(serializers.ModelSerializer):
    cart_items = SubCartSerializer(many=True)
    total_value = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_value(self, obj):
        total = 0
        for cart_item in obj.cart_items.all():
            total += cart_item.qty * cart_item.product.product_selling_price
        return total

    def get_total_items(self, obj):
        return obj.cart_items.aggregate(Sum('qty'))['qty__sum'] or 0

    def get_cart_items(self, obj):
        return obj.cart_items


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


class PhotoOrderSerializer(serializers.ModelSerializer):
    order_image = Base64ImageField(required=False)

    class Meta:
        model = PhotoOrder
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = "__all__"


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'


class RecentProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SubCart
        fields = "__all__"


class OutForDeliverySerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = OutForDelivery
        fields = "__all__"


class OrderStatusSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()

    class Meta:
        model = OrderStatus
        fields = "__all__"

    def get_order_id(self, obj):
        return 12321

# class ProductWithOfferSerializer(serializers.ModelSerializer):
#     product_details = ProductSerializer(source='*', read_only=True)
#     offer_price = serializers.SerializerMethodField()
#     discount = serializers.SerializerMethodField()
#     price_after_discount = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Product
#         fields = ("product_details", "offer_price", "discount", "price_after_discount")
#
#     def get_offer_price(self, product):
#         # Retrieve the lowest offer price for the product
#         lowest_offer = Offers.objects.filter(product=product).order_by('offer_discounted_price').first()
#         if lowest_offer:
#             return lowest_offer.offer_discounted_price
#         return None
#
#     def get_discount(self, product):
#         offer_price = self.get_offer_price(product)
#         if offer_price is not None:
#             return product.product_selling_price - float(offer_price)
#         return 0
#
#     def get_price_after_discount(self, product):
#         offer_price = self.get_offer_price(product)
#         if offer_price is not None:
#             return offer_price
#         return product.product_selling_price


class ProductWithOfferSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='*', read_only=True)
    offer_price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("product_details", "offer_price", "discount", "discount_percentage")

    def get_offer_price(self, product):
        # Retrieve the lowest offer price for the product
        lowest_offer = Offers.objects.filter(product=product).order_by('offer_discounted_price').first()
        if lowest_offer:
            return lowest_offer.offer_discounted_price
        return None

    def get_discount(self, product):
        offer_price = self.get_offer_price(product)
        if offer_price is not None:
            return product.product_selling_price - float(offer_price)
        return 0

    def get_discount_percentage(self, product):
        offer_price = self.get_offer_price(product)
        if offer_price is not None:
            return ((product.product_selling_price - float(offer_price)) / product.product_selling_price) * 100
        return 0
