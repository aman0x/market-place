from rest_framework import serializers
from bazaarApp.models import Bazaar
from agentApp.api.serializers import AgentSerializer
from wholesellerApp.api.serializers import WholesellerSerializer
from agentApp.models  import Agent
from productApp.models import Product
from parentCategoryApp.models import ParentCategory
from drf_extra_fields.fields import Base64ImageField


class BazaarSerializer(serializers.ModelSerializer):
    category_group = serializers.SerializerMethodField(read_only=True)
    wholesellers = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    states = serializers.SerializerMethodField(read_only=True)
    earnings = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)
    bazaar_image = Base64ImageField()
    class Meta:

        model = Bazaar
        fields = '__all__'

    def update(self, validated_data):
        bazaar_image = validated_data.pop('bazaar_image')
        return Bazaar.objects.create(bazaar_image=bazaar_image)
   
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
    
    def get_category_group(self, obj):
        return obj.parent_category_bazaar.all().values('id','parent_category_name')
    
    


class BazaarDashboardSerializer(serializers.ModelSerializer):
    wholesellers = serializers.SerializerMethodField(read_only=True)
    earnings = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    commission = serializers.SerializerMethodField(read_only=True)
    customer = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = '__all__'

    def get_wholesellers(self, obj):
        return obj.wholeseller.count()

    def get_earnings(self,obj):
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
        fields = ['id', 'name', 'city', 'orders', 'sales']

    def get_name(self,obj):
        return obj.wholeseller.all().values_list('wholeseller_name')

    def get_city(self, obj):
        return obj.wholeseller.all().values_list('wholeseller_city__city')
    
    def get_orders(self, obj):
        return 10000

    # def get_orders(self, obj):
    #     orders = obj.bazaar_product.all()
    #     total_orders = orders.count()  
    #     return total_orders


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

    # def get_item(self, obj):
    #     return [product.product_name for product in obj.bazaar_product.all()]

    def get_item(self, obj):
        return obj.product_bazaar.all().values_list('product_name')
    
    def get_price(self, obj):
        return obj.product_bazaar.all().values_list('product_mrp')
    
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
        return obj.product_bazaar.all().values_list('product_name', flat=True)
    
    def get_brand(self, obj):
        return obj.product_bazaar.all().values_list('product_brand_name', flat=True)
    
    def get_group_category(self, obj):
        return obj.parent_category_bazaar.all().values_list('parent_category_name', flat=True)
    
    def get_category(self, obj):
        return obj.category_bazaar.all().values_list('category_name', flat=True)
    
    def get_sub_category(self, obj):
        return obj.subcategory_bazaar.all().values_list('subcategory_name', flat=True)

    def get_weight(self, tsk):
        return '10kg'

    def get_mrp(self, task):
        return '100'
    
    def get_active(self, obj):
        return obj.product_bazaar.all().values_list('product_active', flat=True)


class ProductBulkUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields =  ["product_name","product_brand_name","product_total_weight",
                  "product_unit","product_total_mrp","product_per_unit_weight","product_mrp",
                  "product_updated_by","product_subcategory","product_category","product_category_group"]
