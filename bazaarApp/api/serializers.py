from rest_framework import serializers
from bazaarApp.models import Bazaar
from agentApp.api.serializers import AgentSerializer
from wholesellerApp.api.serializers import WholesellerSerializer



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
