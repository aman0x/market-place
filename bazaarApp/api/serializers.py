from rest_framework import serializers
from bazaarApp.models import Bazaar
from agentApp.api.serializers import AgentSerializer
from wholesellerApp.api.serializers import WholesellerSerializer
from agentApp.models  import Agent
from productApp.models import Product


class BazaarAgentSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(many=True, read_only=True)

    class Meta:
        model = Bazaar
        fields = "__all__"


class BazaarWholesellerSerializer(serializers.ModelSerializer):
    wholeseller = WholesellerSerializer(many=True, read_only=True)

    class Meta:
        model = Bazaar
        fields = "__all__"


class BazaarProductSerializer(serializers.ModelSerializer):
    agent = serializers.StringRelatedField(many=True)

    class Meta:
        model = Bazaar
        fields = "__all__"


class BazaarSerializer(serializers.ModelSerializer):
    wholesellers = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    states = serializers.SerializerMethodField(read_only=True)
    earnings = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = '__all__'

    def get_wholesellers(self, obj):
        return obj.wholeseller.count()

    def get_agents(self, obj):
        return obj.agent.count()
    
   
    def get_states(self, obj):
        return obj.bazaar_state.count()
   
    def get_earnings(self,obj):
        return

    def get_bills(self, obj):
        return
    #     bills = obj.bill.all()
    #     serializer = BillSerializer(bills, many=True)
    #     return serializer.data


class BazaarViewReportTotalOrdersSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id', 'total_orders']

    def get_total_orders(self, task):
        return '910'


class BazaarViewReportTotalIncomeSerializer(serializers.ModelSerializer):
    total_income = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id', 'total_income']

    def get_total_income(self, task):
        return '556690'


class BazaarViewReportCityWiseSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id', 'cities', 'orders', 'sales']

    def get_cities(self, obj):
        return obj.bazaar_city.count()

    def get_orders(self, obj):
        return obj.bazaar_product.count()

    def get_sales(self, obj):
        return
        



class BazaarViewReportTopWholesellersSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id', 'name', 'city', 'orders', 'sales']

    def get_name(self,obj):
        return obj.name

    def get_city(self, obj):
        return obj.bazaar_city.name

    def get_orders(self, obj):
        orders = obj.orders.all()
        total_orders = orders.count()  
        return total_orders


    def get_sales(self, obj):
        return '15302'


class BazaarViewReportTopProductsSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    sold = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id', 'item', 'price', 'sold', 'sales']

    def get_item(self, obj):
        return [product.product_name for product in obj.bazaar_product.all()]


    def get_price(self, task):
        return "100"
        # order_products = obj.orders_set.first().Product.all()  # get all products in the first order associated with the Bazaar object
        # total_price = sum([product.price for product in order_products])  # calculate the total price of all products in the order
        # return total_price if order_products else None

        # products = obj.bazaar_product.all()
        # return [product.price for product in products]
     
    # def get_price(self, obj):
    #     product = obj.bazaar_product.first()
    #     return product.price if product else None

    
    def get_sold(self, task):
        # products = obj.bazaar_product.all()
        # total_sold = sum([product.sold for product in products])
        return "13"

    def get_sales(self, task):
        return '15304'


class BazaarViewReportNewWholesellersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    customer_id = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id', 'username', 'customer_id']

    def get_username(self,task):
        return "user"

    def get_customer_id(self, task):
        return '00010'
    
class AgentSerializers(serializers.ModelSerializer):
    agent=serializers.ReadOnlyField(source='agent_name')
    class Meta:
        model=Agent
        field=['id','agent']

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
        fields = ['id', 'name', 'contact_person','agent',
                  'city', 'bazaar', 'type',
                  'status', 'enable']

    def get_name(self, obj):
        return obj.wholeseller.all().values_list('wholeseller_name', flat=True)
    
    def get_contact_person(self, obj):
        return obj.wholeseller.all().values_list('wholeseller_contact_per', flat=True)

    def get_city(self, obj):
        wholesellers = obj.wholeseller.all()
        cities = wholesellers.values_list('wholeseller_city', flat=True)
        return cities

    def get_bazaar(self, obj):
        return obj.bazaar_name

    def get_type(self, obj):
        wholesellers=obj.wholeseller.all()
        wholeseller_type=wholesellers.values_list('wholeseller_type',flat=True)
        return list(set(wholeseller_type))
        
    def get_agent(self, obj):
        return obj.wholeseller.all().values_list('wholeseller_agent', flat=True)

    def get_status(self, task):
        return 'Created'

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
        fields = ['id', 'name', 'mobile_number',
                   'bazaar', 'city','type',
                  'status', 'enable']
        
    def get_name(self, obj):
        agents = obj.agent.all()
        name = []
        for agent in agents:
            name.append(agent.agent_name)
        return name

    def get_mobile_number(self,obj):
        agents = obj.agent.all()
        number = []
        for agent in agents:
             number.append(str(agent.agent_number.country_code) 
                           + str(agent.agent_number.national_number))
        return number

    def get_city(self, obj):
        agents = obj.agent.all()
        cities = agents.values_list('agent_city', flat=True)
        return cities

    def get_type(self, obj):
        agents=obj.agent.all()
        agent_type=agents.values_list('agent_type',flat=True)
        return list(set(agent_type))

    def get_bazaar(self, obj):
        return obj.bazaar_name

    def get_status(self, task):
        return 'Created'
    
    def get_enable(self, task):
        return True

class BazaarProductsListSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    brand = serializers.SerializerMethodField(read_only=True)
    group_category = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)
    sub_category = serializers.SerializerMethodField(read_only=True)
    weight = serializers.SerializerMethodField(read_only=True)
    mrp = serializers.SerializerMethodField(read_only=True)
    active = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id', 'product_name', 'brand',
                  'group_category', 'category', 'sub_category',
                  'weight', 'mrp', 'active']

    def get_product_name(self, obj):
        products = obj.bazaar_product.all()
        name = []
        for product in products:
            name.append(product.product_name)
        return name

    def get_brand(self, obj):
        products = obj.bazaar_product.all()
        brand = []
        for product in products:
            brand.append(product.product_brand_name)
        return brand

    def get_group_category(self, obj):
        products = obj.bazaar_product.all()
        group_category = products.values_list('product_category_group', flat=True)
        return group_category
    
    def get_category(self, obj):
        products = obj.bazaar_product.all()
        category = products.values_list('product_category', flat=True)
        return category
    
    def get_sub_category(self, obj):
        products = obj.bazaar_product.all()
        sub_category = products.values_list('product_subcategory', flat=True)
        return sub_category

    def get_weight(self, tsk):
        return '10kg'

    def get_mrp(self, task):
        return '100'

    def get_active(self, obj):
        products = obj.bazaar_product.all()
        active = []
        for product in products:
            active.append(product.product_active)
        return active

class ProductBulkUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields =  ["product_name","product_brand_name","product_total_weight",
                  "product_unit","product_total_mrp","product_per_unit_weight","product_mrp",
                  "product_updated_by","product_subcategory","product_category","product_category_group"]
