from rest_framework import serializers

import categoryApp.models
from wholesellerApp.models import *
from bazaarApp.models import Bazaar
from retailerApp.models import Retailer
from productApp.models import Product
from drf_extra_fields.fields import Base64ImageField
from bazaarApp.api.serializers import BazaarSerializer
from locationApp.models import *
from planApp.models import Plan
from paymentApp.models import Payment
from masterApp.models import WholesellerType
from locationApp.api.serializers import *
from productApp.models import Product
from productApp.api.serializers import ProductSerializer
from categoryApp.models import Category
from categoryApp.api.serializers import CategorySerializer
from subCategoryApp.models import SubCategory
from subCategoryApp.api.serializers import SubCategorySerializer
from masterApp.api.serializers import RetailerTypeSerializer

# from locationApp.models import *


class WholesellerSerializer(serializers.ModelSerializer):
    wholeseller_adhar_front_image = Base64ImageField(required=False)
    wholeseller_adhar_back_image = Base64ImageField(required=False)
    wholeseller_pan_card_image = Base64ImageField(required=False)
    wholeseller_image = Base64ImageField(required=False)
    wholeseller_bazaar_data = serializers.SerializerMethodField()
    wholeseller_state_name = serializers.SerializerMethodField()
    wholeseller_district_name = serializers.SerializerMethodField()
    wholeseller_city_name = serializers.SerializerMethodField()
    wholeseller_plan_name = serializers.SerializerMethodField()
    wholeseller_payment_name = serializers.SerializerMethodField()
    wholeseller_type_name = serializers.SerializerMethodField()

    # Wholeseller_created_agent = serializers.SerializerMethodField()

    class Meta:
        model = Wholeseller
        fields = '__all__'

    def get_Wholeseller_created_agent(self, obj):
        wholeseller_agents = WholesellerAgent.objects.filter(wholeseller=obj)
        serializer = WholesellerIdAgentSerializer(wholeseller_agents, many=True)
        return serializer.data

    def get_wholeseller_state_name(self, obj):
        state = ""
        state_id = obj.wholeseller_state_id
        if state_id is not None:
            state = State.objects.filter(id=state_id).get().state
        return state

    def get_wholeseller_district_name(self, obj):
        district = ""
        district_id = obj.wholeseller_district_id
        if district_id is not None:
            district = District.objects.filter(id=district_id).get().district
        return district

    def get_wholeseller_city_name(self, obj):
        city = ""
        city_id = obj.wholeseller_city_id
        if city_id is not None:
            city = City.objects.filter(id=city_id).get().city
        return city

    def get_wholeseller_bazaar_data(self, obj):
        bazaar_ids = obj.wholeseller_bazaar.all()
        bazaar = Bazaar.objects.filter(id__in=bazaar_ids)
        serializer = BazaarSerializer(bazaar, many=True)
        return serializer.data

    def get_wholeseller_plan_name(self, obj):
        plan = ""
        try:
            plan_id = obj.wholeseller_plan_id
        except:
            plan_id = None
        if plan_id is not None:
            plan = Plan.objects.filter(id=plan_id).get().plan_name
        return plan

    def get_wholeseller_payment_name(self, obj):
        payment = ""
        payment_id = obj.wholeseller_payment_id
        if payment_id is not None:
            payment = Payment.objects.filter(id=payment_id).get().payment_choice
        return payment

    def get_wholeseller_type_name(self, obj):
        wholeseller_type = ""
        wholeseller_type_id = obj.wholeseller_type_id
        if wholeseller_type_id is not None:
            wholeseller_type = WholesellerType.objects.filter(id=wholeseller_type_id).get().wholeseller_type_name
        return wholeseller_type

    def update(self, instance, validated_data):
        instance.wholeseller_adhar_front_image = validated_data.get(
            'wholeseller_adhar_front_image')
        instance.wholeseller_adhar_back_image = validated_data.get(
            'wholeseller_adhar_back_image')
        instance.wholeseller_pan_card_image = validated_data.get(
            'wholeseller_pan_card_image')
        instance.wholeseller_image = validated_data.get(
            'wholeseller_image')
        event = super().update(instance, validated_data)
        return event


class Wholeseller_bazzarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = ["wholeseller_bazaar"]


class WholesellerViewReportCityWiseSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wholeseller
        fields = ['id', 'cities', 'orders', 'sales']
        # fields = ['id', 'orders', 'sales']

    def get_cities(self, obj):
        city = obj.wholeseller_city.city
        return city

    def get_orders(self, obj):
        return 12000

    def get_sales(self, obj):
        return 10000


class WholesellerViewReportRetailerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    customer_id = serializers.SerializerMethodField()


class WholesellerDashboardTopRetailersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = "__all__"


class WholelsellerBazaarListSerializer(serializers.ModelSerializer):
    wholeseller_bazaar_data = serializers.SerializerMethodField()

    class Meta:
        model = Wholeseller
        fields = ["wholeseller_bazaar_data"]

    def get_wholeseller_bazaar_data(self, obj):
        bazaar_ids = obj.wholeseller_bazaar.all()
        bazaar_names = []
        for bazaar in bazaar_ids:
            bazaar_name = Bazaar.objects.filter(id=bazaar.id).get().bazaar_name
            bazaar_data = {"bazaar_id": bazaar.id, "bazaar_name": bazaar_name}
            bazaar_names.append(bazaar_data)
        return bazaar_names


class WholesellerBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        # fields = ['branch_name', 'manager_name', 'branch_phone']


class WholesellerBazaarProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_stock(self, obj):
        stock = obj.product_stocks
        if stock == None or 0:
            stocks = "Out of Stock"
        else:
            stocks = "Available"
        return stocks


class WholesellerBazaarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bazaar
        fields = "__all__"


# =====================   wholeseller agent

class WholesellerIdAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WholesellerAgent
        fields = '__all__'


class WholesellerAgentSerializer(serializers.ModelSerializer):
    agent_image = Base64ImageField(required=False)
    agent_adhar_front_image = Base64ImageField(required=False)
    agent_adhar_back_image = Base64ImageField(required=False)
    product_upload_mrp_label_image = Base64ImageField(required=False)
    agent_pancard_image = Base64ImageField(required=False)
    agent_agency_name = serializers.SerializerMethodField()
    agent_bazaar_data = serializers.SerializerMethodField()
    wholeseller_agent_assigned_state_names = serializers.SerializerMethodField()
    wholeseller_agent_assigned_district_names = serializers.SerializerMethodField()
    wholeseller_agent_assigned_city_names = serializers.SerializerMethodField()
    wholeseller_agent_city_name = serializers.SerializerMethodField()
    agent_district_name = serializers.SerializerMethodField()
    agent_state_name = serializers.SerializerMethodField()

    class Meta:
        model = WholesellerAgent
        fields = '__all__'

    def get_agent_agency_name(self, obj):
        firm_name = ""
        agency_id = obj.agency_id
        if agency_id is not None:
            firm_name = Agency.objects.filter(id=agency_id).get().firm_name
        return firm_name

    def get_agent_state_name(self, obj):
        state = ""
        state_id = obj.wholeseller_agent_state_id
        if state_id is not None:
            state = State.objects.filter(id=state_id).get().state
        return state

    def get_agent_district_name(self, obj):
        district = ""
        district_id = obj.wholeseller_agent_district_id
        if district_id is not None:
            district = District.objects.filter(id=district_id).get().district
        return district

    def get_wholeseller_agent_city_name(self, obj):
        city = ""
        city_id = obj.wholeseller_agent_city_id
        if city_id is not None:
            city = City.objects.filter(id=city_id).get().city
        return city

    def get_agent_bazaar_data(self, obj):
        bazaar_ids = obj.wholeseller_agent_bazaar.all()
        bazaar = Bazaar.objects.filter(id__in=bazaar_ids)
        serializer = BazaarSerializer(bazaar, many=True)
        return serializer.data

    def get_wholeseller_agent_assigned_state_names(self, obj):
        state_ids = obj.wholeseller_agent_assigned_state.all()
        states = State.objects.filter(id__in=state_ids)
        serializer = StateSerializer(states, many=True)
        return serializer.data

    def get_wholeseller_agent_assigned_district_names(self, obj):
        district_ids = obj.wholeseller_agent_assigned_district.all()
        district = District.objects.filter(id__in=district_ids)
        serializer = DistrictSerializer(district, many=True)
        return serializer.data

    def get_wholeseller_agent_assigned_city_names(self, obj):
        city_ids = obj.wholeseller_agent_assigned_city.all()
        city = City.objects.filter(id__in=city_ids)
        serializer = CitySerializer(city, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        instance.agent_image = validated_data.get(
            'agent_image')
        instance.agent_adhar_front_image = validated_data.get(
            'agent_adhar_front_image')
        instance.agent_adhar_back_image = validated_data.get(
            'agent_adhar_back_image')
        instance.agent_pancard_image = validated_data.get(
            'agent_pancard_image')
        event = super().update(instance, validated_data)
        return event


# ---------------- wholeseller branch product ---------
class BranchProductSerializer(serializers.ModelSerializer):
    # product_details = serializers.SerializerMethodField()
    class Meta:
        model = Branch_Product
        fields = '__all__'
        # exclude = ['branch']

    def validate(self, attrs):
        branch = attrs.get('branch')
        if branch and branch.main_branch:
            return attrs
        raise serializers.ValidationError("Branch must be a main branch.")

    def get_product_details(self, obj):
        product = Product.objects.filter(id=obj.product_id)
        serializer = ProductSerializer(product, many=True)
        return serializer.data


class BranchCategoryWisePlanSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    subCategory_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    retailer_details = serializers.SerializerMethodField()


    class Meta:
        model = Branch_Category_Wise_Plan
        fields = '__all__'

    def get_subCategory_name(self, obj):
        subCategory = SubCategory.objects.filter(id=obj.category_id)
        serializer = SubCategorySerializer(subCategory, many=True)
        serialized_data = serializer.data
        subcategory_names = [data['subcategory_name'] for data in serialized_data]
        return subcategory_names

    def get_branch_name(self, obj):
        branch = Branch.objects.filter(id=obj.branch_id)
        serializer = WholesellerBranchSerializer(branch, many=True)
        serialized_data = serializer.data
        branch_name = [data['branch_name'] for data in serialized_data]
        return branch_name


    def get_category_name(self, obj):
        category = Category.objects.filter(id=obj.category_id)
        serializer = CategorySerializer(category, many=True)
        serialized_data = serializer.data
        category_name = [data['category_name'] for data in serialized_data]
        return category_name

    def get_retailer_details(self, obj):
        retailer_type_ids = obj.retailer_type.all()
        retailer_type = RetailerType.objects.filter(id__in=retailer_type_ids)
        serializer = RetailerTypeSerializer(retailer_type, many=True)
        return serializer.data

class BranchSubCategoryWisePlanSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    retailer_details = serializers.SerializerMethodField()

    class Meta:
        model = Branch_Sub_Category_Wise_Plan
        fields = '__all__'

    def get_retailer_details(self, obj):
        retailer_type_ids = obj.retailer_type.all()
        retailer_type = RetailerType.objects.filter(id__in=retailer_type_ids)
        serializer = RetailerTypeSerializer(retailer_type, many=True)
        return serializer.data

    def get_product_details(self, obj):
        product = Product.objects.filter(id=obj.sub_category_id)
        serializer = ProductSerializer(product, many=True)
        return serializer.data


class BranchItemWisePlanSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    retailer_details = serializers.SerializerMethodField()
    class Meta:
        model = Branch_Item_Wise_Plan
        fields = '__all__'
        # exclude = ['customer_type']

    def get_retailer_details(self, obj):
        retailer_type_ids = obj.retailer_type.all()
        retailer_type = RetailerType.objects.filter(id__in=retailer_type_ids)
        serializer = RetailerTypeSerializer(retailer_type, many=True)
        return serializer.data

    def get_product_details(self, obj):
        product_ids = obj.product.all()
        product = Product.objects.filter(id__in=product_ids)
        serializer = ProductSerializer(product, many=True)
        return serializer.data


class BranchProductPricingSerializer(serializers.ModelSerializer):
    product_total_mrp = serializers.ReadOnlyField(source='product.product_total_mrp')

    class Meta:
        model = Branch_Product_Pricing
        fields = ['id', 'product', 'new_base_price', 'last_update_date', 'product_total_mrp']
class BranchProductPricingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch_Product_Pricing
        fields = ['product', 'new_base_price']

class BranchProductPricingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch_Product_Pricing
        fields = ['new_base_price']


class OrderSerializer(serializers.ModelSerializer):
    retailer_details = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__'

    def get_retailer_details(self, obj):
        retailer_type_ids = obj.retailer_type.all()
        retailer_type = RetailerType.objects.filter(id__in=retailer_type_ids)
        serializer = RetailerTypeSerializer(retailer_type, many=True)
        return serializer.data

class EditOrderSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = EditOrder
        fields = '__all__'

    def get_product_details(self, obj):
        product_id = obj.product_id
        product = Product.objects.filter(id=product_id)
        serializer = ProductSerializer(product, many=True)
        return serializer.data


    def get_order_details(self,obj):
        order_id = obj.order_id.id
        order = Order.objects.filter(id=order_id)
        serializer = OrderSerializer(order, many=True)
        return serializer.data


class OfferSerializer(serializers.ModelSerializer):
    offer_name = serializers.SerializerMethodField()
    offer_image = Base64ImageField(required=False)

    class Meta:
        model = Offers
        fields = '__all__'

    def get_offer_name(self, obj):
        try:
            name = obj.product.product_name
        except:
            name = "None"
        return name

    def update(self, instance, validated_data):
        instance.offer_image = validated_data.get('offer_image')
        event = super().update(instance, validated_data)
        return event

class OfferDetailsSerializer(serializers.ModelSerializer):
    offer_name = serializers.SerializerMethodField()
    offer_image = Base64ImageField(required=False)
    productIdetails = ProductSerializer(source='product')

    class Meta:
        model = Offers
        fields = '__all__'

    def get_offer_name(self, obj):
        try:
            name = obj.product.product_name
        except:
            name = "None"
        return name

