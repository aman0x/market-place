from rest_framework import serializers
from agentApp.models import Agent
from productApp.models import Product,ParentCategory,Category,SubCategory,Bazaar
from drf_extra_fields.fields import Base64ImageField
from locationApp.api.serializers import *
from locationApp.models import *


class BazaarSerializer(serializers.ModelSerializer):
    category_group = serializers.SerializerMethodField(read_only=True)
    wholesellers = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    states = serializers.SerializerMethodField(read_only=True)
    earnings = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)
    bazaar_image = Base64ImageField(required=False)
    bazaar_state_names = serializers.SerializerMethodField()
    bazaar_district_names = serializers.SerializerMethodField()
    bazaar_city_names = serializers.SerializerMethodField()

    class Meta:
        model = Bazaar
        fields = "__all__"

    def get_bazaar_state_names(self, obj):
        state_ids = obj.bazaar_state.all()
        states = State.objects.filter(id__in=state_ids)
        serializer = StateSerializer(states, many=True)
        return serializer.data

    def get_bazaar_district_names(self, obj):
        district_ids = obj.bazaar_district.all()
        district = District.objects.filter(id__in=district_ids)
        serializer = DistrictSerializer(district, many=True)
        return serializer.data

    def get_bazaar_city_names(self, obj):
        city_ids = obj.bazaar_city.all()
        city = City.objects.filter(id__in=city_ids)
        serializer = CitySerializer(city, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        instance.bazaar_image = validated_data.get("bazaar_image")
        event = super().update(instance, validated_data)
        return event

    def get_wholesellers(self, obj):
        return obj.wholeseller.count()

    def get_agents(self, obj):
        return obj.agent.count()

    def get_states(self, obj):
        return obj.bazaar_state.count()

    def get_earnings(self, obj):
        return

    def get_bills(self, obj):
        return

    def get_category_group(self, obj):
        return obj.parent_category_bazaar.all().values("id", "parent_category_name")


class BazaarDashboardSerializer(serializers.ModelSerializer):
    wholesellers = serializers.SerializerMethodField(read_only=True)
    earnings = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    commission = serializers.SerializerMethodField(read_only=True)
    customer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = "__all__"

    def get_wholesellers(self, obj):
        return obj.wholeseller.count()

    def get_earnings(self, obj):
        return

    def get_bills(self, obj):
        return

    def get_agents(self, obj):
        return obj.agent.count()

    def get_commission(self, obj):
        return

    def get_customer(self, obj):
        return


class BazaarViewReportTotalOrdersSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = ["id", "total_orders"]

    def get_total_orders(self, task):
        return "910"


class BazaarViewReportTotalIncomeSerializer(serializers.ModelSerializer):
    total_income = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = ["id", "total_income"]

    def get_total_income(self, task):
        return "556690"


class BazaarViewReportCityWiseSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = ["id", "cities", "orders", "sales"]

    def get_cities(self, obj):
        return obj.bazaar_city.count()

    def get_orders(self, obj):
        return 12000

    def get_sales(self, obj):
        return 10000


class BazaarViewReportTopWholesellersSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = ["id", "name", "city", "orders", "sales"]

    def get_name(self, obj):
        return obj.wholeseller.all().values_list("wholeseller_name")

    def get_city(self, obj):
        return obj.wholeseller.all().values_list("wholeseller_city__city")

    def get_orders(self, obj):
        return 10000

    # def get_orders(self, obj):
    #     orders = obj.bazaar_product.all()
    #     total_orders = orders.count()
    #     return total_orders

    def get_sales(self, obj):
        return "15302"


class BazaarViewReportTopProductsSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    sold = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = ["id", "item", "price", "sold", "sales"]

    # def get_item(self, obj):
    #     return [product.product_name for product in obj.bazaar_product.all()]

    def get_item(self, obj):
        return obj.product_bazaar.all().values_list("product_name")

    def get_price(self, obj):
        return obj.product_bazaar.all().values_list("product_mrp")

    def get_sold(self, task):
        # products = obj.bazaar_product.all()
        # total_sold = sum([product.sold for product in products])
        return "13"

    def get_sales(self, task):
        return "15304"


class BazaarViewReportNewWholesellersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    customer_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = ["id", "username", "customer_id"]

    def get_username(self, task):
        return "user"

    def get_customer_id(self, task):
        return "00010"


class AgentSerializers(serializers.ModelSerializer):
    agent = serializers.ReadOnlyField(source="agent_name")

    class Meta:
        model = Agent
        field = ["id", "agent"]


class BazaarWholesellersListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    contact_person = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    bazaar = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    enable = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = [
            "id",
            "name",
            "contact_person",
            "agent",
            "city",
            "bazaar",
            "type",
            "status",
            "enable",
        ]

    def get_name(self, obj):
        return obj.wholeseller.all().values_list("wholeseller_name", flat=True)

    def get_contact_person(self, obj):
        return obj.wholeseller.all().values_list("wholeseller_contact_per", flat=True)

    def get_city(self, obj):
        wholesellers = obj.wholeseller.all()
        cities = wholesellers.values_list("wholeseller_city", flat=True)
        return cities

    def get_bazaar(self, obj):
        return obj.bazaar_name

    def get_type(self, obj):
        wholesellers = obj.wholeseller.all()
        wholeseller_type = wholesellers.values_list("wholeseller_type", flat=True)
        return list(set(wholeseller_type))

    def get_agent(self, obj):
        return obj.wholeseller.all().values_list("wholeseller_agent", flat=True)

    def get_status(self, task):
        return "Created"

    def get_enable(self, task):
        return True


class BazaarAgentsListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    mobile_number = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    bazaar = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    enable = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bazaar
        fields = [
            "id",
            "name",
            "mobile_number",
            "bazaar",
            "city",
            "type",
            "status",
            "enable",
        ]

    def get_name(self, obj):
        agents = obj.agent.all()
        name = []
        for agent in agents:
            name.append(agent.agent_name)
        return name

    def get_mobile_number(self, obj):
        agents = obj.agent.all()
        number = []
        for agent in agents:
            number.append(
                str(agent.agent_number.country_code)
                + str(agent.agent_number.national_number)
            )
        return number

    def get_city(self, obj):
        agents = obj.agent.all()
        cities = agents.values_list("agent_city", flat=True)
        return cities

    def get_type(self, obj):
        agents = obj.agent.all()
        agent_type = agents.values_list("agent_type", flat=True)
        return list(set(agent_type))

    def get_bazaar(self, obj):
        return obj.bazaar_name

    def get_status(self, task):
        return "Created"

    def get_enable(self, task):
        return True


class BazaarProductsListSerializer(serializers.ModelSerializer):
    bazaar_name = serializers.SerializerMethodField()
    category_group_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "product_brand_name",
            "bazaar_name",
            "category_group_name",
            "category_name",
            "subcategory_name",
            "product_total_weight",
            "product_total_mrp",
            "product_active",
            "bazaar",
            "category_group",
            "category",
            "subcategory",
        ]

    def get_bazaar_name(self, obj):
        bazaar_name = ""
        bazaar_id = obj.bazaar_id
        if bazaar_id is not None:
            bazaar_name = Bazaar.objects.filter(id=bazaar_id).get().bazaar_name
        return bazaar_name
    
    def get_category_group_name(self, obj):
        category_group_name = ""
        category_group_id = obj.category_group_id
        if category_group_id is not None:
            category_group_name = ParentCategory.objects.filter(id=category_group_id).get().parent_category_name
        return category_group_name
    
    def get_category_name(self, obj):
        category_name = ""
        category_id = obj.category_id
        if category_id is not None:
            category_name = Category.objects.filter(id=category_id).get().category_name
        return category_name
    
    def get_subcategory_name(self, obj):
        subcategory_name = ""
        subcategory_id = obj.subcategory_id
        if subcategory_id is not None:
            subcategory_name = SubCategory.objects.filter(id=subcategory_id).get().subcategory_name
        return subcategory_name

class ProductBulkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "product_name",
            "product_brand_name",
            "product_total_weight",
            "product_unit",
            "product_total_mrp",
            "product_per_unit_weight",
            "product_mrp",
            "product_updated_by",
            "product_subcategory",
            "product_category",
            "product_category_group",
        ]
