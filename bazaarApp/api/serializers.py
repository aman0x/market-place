from rest_framework import serializers
from bazaarApp.models import Bazaar
from agentApp.api.serializers import AgentSerializer
from wholesellerApp.api.serializers import WholesellerSerializer
from rest_framework import filters
from django.db.models import Count,Sum
from agentApp.models  import Agent



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
        fields = ['id', 'name', 'contact_person',
                  'city', 'bazaar', 'type','agent',
                  'status', 'enable']

    def get_name(self, obj):
            return obj.wholeseller.all().values_list('wholeseller_name', flat=True)


    def get_contact_person(self, obj):
            wholesellers = obj.wholeseller.all()

            if wholesellers.exists():
                return wholesellers.first().wholeseller_contact_per.all()
            return None



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
       wholesellers = obj.wholeseller.all()
       agent_name = wholesellers.values_list('wholeseller_agent', flat=True)
       agent_serializer = AgentSerializer(agent_name, many=True)
       return agent_serializer.data
          
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
                  'city', 'bazaar', 'type',
                  'status', 'enable']

    
    def get_name(self, obj):
        agents = obj.agent.all()
        if agents.exists():
            return ', '.join(agent.agent_name for agent in agents.all())
        else:
            return 'Unknown'


    # def get_mobile_number(self, obj):
    #     agents = obj.agent.all()
    #     if agents.exists():
    #         return str(', '.join(agent.agent_number for agent in agents.all()))
    #     else:
    #         return ''
    #       return str(obj.mobile_number) if obj.mobile_number else ''
    def get_mobile_number(self,obj):
           return str(obj.mobile_number) if obj.mobile_number else ''


    def get_city(self, obj):
        agents = obj.agent.all()
        if agents.exists():
            return ', '.join(agent.agent_city.city_name for agent in agents.all())
        else:
            return ''



    def get_bazaar(self, obj):
        return obj.bazaar_name

    def get_type(self, obj):
        return obj.agent_type if obj.agent_type else 'Unknown'

        

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
