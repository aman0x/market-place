from rest_framework import serializers
from bazaarApp.models import Bazaar
from agentApp.api.serializers import AgentSerializer
from wholesellerApp.api.serializers import WholesellerSerializer
from rest_framework import filters



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
        
    def get_wholesellers(self, task):
        return '20'
    
    def get_agents(self, task):
        return '13'
    
    def get_states(self, task):
        return '2'
    
    def get_earnings(self, task):
        return '154000'
    
    def get_bills(self, task):
        return '52'
    
class BazaarViewReportTotalOrdersSerializer(serializers.ModelSerializer):
    total_orders = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id','total_orders']
        
    def get_total_orders(self, task):
        return '910'
    
class BazaarViewReportTotalIncomeSerializer(serializers.ModelSerializer):
    total_income = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id','total_income']
        
    def get_total_income(self, task):
        return '556690'
    
class BazaarViewReportCityWiseSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id','cities','orders','sales']
        
    def get_cities(self, task):
        return 'Delhi'
    
    def get_orders(self, task):
        return '12202'
    
    def get_sales(self, task):
        return '150200'

    
class BazaarViewReportTopWholesellersSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id','name','city','orders','sales']
        
    def get_name(self, task):
        return 'Wingreens Mart'
    
    def get_city(self, task):
        return '49'
    
    def get_orders(self, task):
        return '5951'
    
    def get_sales(self, task):
        return '15302'

class BazaarViewReportTopProductsSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    sold = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id','item','price','sold','sales']
        
    def get_item(self, task):
        return 'Amazon Echo'
    
    def get_price(self, task):
        return '53'
    
    def get_sold(self, task):
        return '5958'
    
    def get_sales(self, task):
        return '15304'

class BazaarViewReportNewWholesellersSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    customer_id = serializers.SerializerMethodField(read_only=True)

    class Meta:

        model = Bazaar
        fields = ['id','username','customer_id']
        
    def get_username(self, task):
        return 'Aiden Murray'
    
    def get_customer_id(self, task):
        return '00010'

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
        fields = ['id','name','contact_person',
                  'city','bazaar','type','agent',
                  'status','enable']
        
    def get_name(self, task):
        return 'Global Mart'
    
    def get_contact_person(self, task):
        return 'Ashish Patel'
    
    def get_city(self, task):
        return 'Rajkot'
    
    def get_bazaar(self, task):
        return 'Electronic Bazaar'
    
    def get_type(self, task):
        return 'Wholeseller'
    
    def get_agent(self, task):
        return 'Ashish Patel'
    
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
        fields = ['id','name','mobile_number',
                  'city','bazaar','type',
                  'status','enable']
        
    def get_name(self, task):
        return 'Ashish Patel'
    
    def get_mobile_number(self, task):
        return '+91-8477852310'
    
    def get_city(self, task):
        return 'Rajkot'
    
    def get_bazaar(self, task):
        return 'Electronic Bazaar'
    
    def get_type(self, task):
        return 'Salesman'
    
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
        fields = ['id','product_name','brand',
                  'group_category','category','sub_category',
                  'weight','mrp','active']
        
    def get_product_name(self, task):
        return 'Amazon Echo'
    
    def get_brand(self, task):
        return 'amazon'
    
    def get_group_category(self, task):
        return 'electronics'
    
    def get_category(self, task):
        return 'electronics'
    
    def get_sub_category(self, task):
        return 'electronics'
    
    def get_weight(self, task):
        return '1 Kg'
    
    def get_mrp(self, task):
        return '15302'
    
    def get_active(self, task):
        return True