import random
from datetime import timedelta, datetime
from rest_framework import viewsets, views
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *
from wholesellerApp.models import Wholeseller
from wholesellerApp.models import Branch
from productApp.models import Product
from adsApp.models import Ads
from bazaarApp.models import Bazaar
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.db.models import Q
from retailerApp.models import Retailer
from categoryApp.models import Category
from categoryApp.api.serializers import CategorySerializer
from subCategoryApp.models import SubCategory
from subCategoryApp.api.serializers import SubCategorySerializer
from django.shortcuts import get_object_or_404


common_status = settings.COMMON_STATUS
contact_number = settings.ADMIN_CONTACT_NUMBER
email = settings.ADMIN_EMAIL


class WholesellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Wholeseller.objects.all()
    serializer_class = WholesellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["wholeseller_name"]


class WholesellerVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        wholeseller_number = request.data.get("wholeseller_number")
        wholeseller_otp = request.data.get("wholeseller_otp")

        try:
            wholeseller = Wholeseller.objects.get(wholeseller_number=wholeseller_number)
            if wholeseller.wholeseller_otp == int(wholeseller_otp):
                # OTP is valid
                wholeseller.wholeseller_otp = None
                wholeseller.save(update_fields=["wholeseller_otp"])
                # Get the User object associated with the Wholeseller
                user = wholeseller.wholeseller_user
                access_token = AccessToken.for_user(user)
                access_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=6400)
                )
                refresh_token = RefreshToken.for_user(user)
                refresh_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=166400)
                )
                return Response(
                    {
                        "access_token": str(access_token),
                        "refresh_token": str(refresh_token),
                        "wholeseller_id": wholeseller.id,
                    }
                )
            else:
                status_code = common_status["unauthorized"]["code"]
                payload = {"details": "Invalid OTP."}
                return Response(payload, status=status_code)
        except Wholeseller.DoesNotExist:
            # Wholeseller not found
            payload = {"details": "Wholeseller not found"}
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)


class WholesellerVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        wholeseller_number = data.get("wholeseller_number")
        password = data.get("wholeseller_otp")
        payload = {}
        if wholeseller_number != "":
            wholeseller_otp = random.randrange(000000, 999999)
            try:
                data = Wholeseller.objects.get(wholeseller_number=wholeseller_number)
                data.wholeseller_otp = wholeseller_otp
                data.save(update_fields=["wholeseller_otp"])
                if data:
                    user = User.objects.filter(id=data.wholeseller_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": wholeseller_otp,
                            "details": "Wholeseller OTP sent of registered mobile Number",
                        }
                        status_code = common_status["success"]["code"]
                    else:
                        payload = {"details": "No user found for the wholeseller"}
                        status_code = common_status["not_found"]["code"]
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
                    status_code = common_status["not_found"]["code"]

            except Wholeseller.DoesNotExist:
                payload = {"details": "Wholeseller not found"}
                status_code = common_status["unauthorized"]["code"]

        else:
            payload = {"details": "Something went wrong."}
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]

        return Response(payload, status=status_code)


class WholesellerApplicationStatusViews(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        wholeseller_number = request.data.get("wholeseller_number")
        wholeseller_status = request.data.get("wholeseller_status")
        kyc_remarks = request.data.get("kyc_remarks")
        try:
            wholeseller = Wholeseller.objects.get(wholeseller_number=wholeseller_number)
            user = wholeseller.wholeseller_user
            if user is None:
                return Response({"message": "Wholeseller user not found."})

            if wholeseller_status == "CREATED":
                message = f"Your application_id {wholeseller_number} is in process. If you have any Query? Fell free to contact Us ."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif wholeseller_status == "PENDING":
                message = f"Your application_id {wholeseller_number} is in process. we have received your Application, Our team is reviewing it. Thank You for your patience .if you have any Query? Fell free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif wholeseller_status == "KYCREJECTED" and kyc_remarks is not None:
                message = f"Your application_id {wholeseller_number} is rejected ! {kyc_remarks}. If you have any Query? Feel free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif wholeseller_status == "KYCAPPROVED":
                message = f"Your application_id {wholeseller_number} is approved !  If you have any Query? Feel free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            else:
                return Response({"message": "Invalid wholeseller status."})
        except Wholeseller.DoesNotExist:
            return Response({"message": "Wholeseller not found."})


class WholesellerDashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Wholeseller.objects.all()
    serializer_class = WholesellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["wholeseller_type"]


class WholesellerReportTotalOrderViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        return Response({"total order": 210})


class WholesellerReportTotalIncomeViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        return Response({"total Income": 5123431})


class WholesellerReportCityWiseBusinessViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WholesellerViewReportCityWiseSerializer
    queryset = Wholeseller.objects.all().order_by("id")

    def get(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(pk=pk)
        return queryset


class WholesellerReportTopProductViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        wholeseller_queryset = Wholeseller.objects.filter(id=pk)
        data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
        product_ids = []
        payload = []
        new_data = []
        count = 0
        for bazaar_id in data:
            Product_queryset = Product.objects.filter(bazaar=bazaar_id)
            for product in Product_queryset:
                id = product.id
                product_ids.append(id)
        for id in product_ids:
            product = Product.objects.filter(id=id)
            Product_data = product.all().values()
            for Product_data in Product_data:
                data = {
                    "product_name": Product_data["product_name"],
                    "product_total_mrp": Product_data["product_total_mrp"],
                    "sold": 12131,
                    "sales": 21213414,
                }
                new_data.append(data)
                payload.append(Product_data)
                count += 1
        return Response({"count": count, "result": new_data})


class WholesellerReportRetailersViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        data = [
            {"Name": "Ajay", "customer_id": 111},
            {"Name": "B", "customer_id": 112},
            {"Name": "Ajay", "customer_id": 122},
        ]
        return Response(data)


class WholesellerReportTransactionViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        data = [
            {
                "payment#123": 124,
                "payment#125": 324,
            }
        ]
        return Response(data)


class WholesellerReportRealtimeSaleViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        data = [{"Orders": 1231, "Avg. Sales per Day": 231312}]
        return Response(data)


class WholesellerProductViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # serializer_class = WholesellerProductSerializer
    # lookup_field = 'id'

    def get(self, request, pk):
        category = request.query_params.get("category")
        subcategory = request.query_params.get("subcategory")
        wholeseller_queryset = Wholeseller.objects.filter(id=pk)
        data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
        product_ids = []
        payload = []
        count = 0
        for bazaar_id in data:
            Product_queryset = Product.objects.filter(bazaar=bazaar_id)
            for product in Product_queryset:
                id = product.id
                product_ids.append(id)

        for id in product_ids:
            if category != "" and subcategory == "":
                product = Product.objects.filter(Q(id=id) & Q(category_id=category))
            elif subcategory != "" and category == "":
                product = Product.objects.filter(
                    Q(id=id) & Q(subcategory_id=subcategory)
                )
            elif subcategory is None and category is None:
                product = Product.objects.filter(id=id)
            elif subcategory != "" and category != "":
                product = Product.objects.filter(
                    Q(id=id) & Q(subcategory_id=subcategory) & Q(category_id=category)
                )
            elif subcategory == "" and category == "":
                product = Product.objects.filter(id=id)

            Product_data = product.all().values()
            for Product_data in Product_data:
                payload.append(Product_data)
                count += 1

        return Response({"count": count, "result": payload})


class WholesellerDashboardBazzarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Wholeseller.objects.all()
    serializer_class = Wholeseller_bazzarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["wholeseller_type"]


class WholesellerDashboardTotalProductViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        category = request.query_params.get("category")
        subcategory = request.query_params.get("subcategory")
        wholeseller_queryset = Wholeseller.objects.filter(id=pk)
        data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
        product_ids = []
        payload = []
        count = 0
        for bazaar_id in data:
            Product_queryset = Product.objects.filter(bazaar=bazaar_id)
            for product in Product_queryset:
                id = product.id
                product_ids.append(id)

        for id in product_ids:
            if category != "" and subcategory == "":
                product = Product.objects.filter(Q(id=id) & Q(category_id=category))
            elif subcategory != "" and category == "":
                product = Product.objects.filter(
                    Q(id=id) & Q(subcategory_id=subcategory)
                )
            elif subcategory is None and category is None:
                product = Product.objects.filter(id=id)
            elif subcategory != "" and category != "":
                product = Product.objects.filter(
                    Q(id=id) & Q(subcategory_id=subcategory) & Q(category_id=category)
                )
            elif subcategory == "" and category == "":
                product = Product.objects.filter(id=id)

            Product_data = product.all().values()
            for Product_data in Product_data:
                payload.append(Product_data)
                count += 1

        return Response({"Total Products": count, "Product Ids": product_ids})


class WholesellerDashboardTotalOrderViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        return Response({"total order": 210})


class WholesellerDashboardTotalIncomeViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        return Response({"total revenue": 425210})


class WholesellerDashboardNewRetailersViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        return Response({"New Retailers": 14})


class WholesellerDashboardTopRetailersViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Retailer.objects.all().order_by("id")
    serializer_class = WholesellerDashboardTopRetailersSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(retailer_wholeseller=pk)
        return queryset


class WholesellerDashboardTopProductsViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        wholeseller_queryset = Wholeseller.objects.filter(id=pk)
        data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
        product_ids = []
        payload = []
        new_data = []
        count = 0
        for bazaar_id in data:
            Product_queryset = Product.objects.filter(bazaar=bazaar_id)
            for product in Product_queryset:
                id = product.id
                product_ids.append(id)
        for id in product_ids:
            product = Product.objects.filter(id=id)
            Product_data = product.all().values()
            for Product_data in Product_data:
                data = {
                    "product_name": Product_data["product_name"],
                    "product_total_mrp": Product_data["product_total_mrp"],
                    "sold": 12131,
                    "sales": 21213414,
                }
                new_data.append(data)
                payload.append(Product_data)
                count += 1
        return Response({"count": count, "result": new_data})


class WholesellerDashboardCategoriesViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        wholeseller_queryset = Wholeseller.objects.filter(id=pk)
        data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
        category_names = []
        new_data = []
        for bazaar_id in data:
            product_queryset = Product.objects.filter(bazaar=bazaar_id)
            for product in product_queryset:
                data = {
                    "category_name": product.category.category_name,
                    "most_purchased_by": "abc limited",
                    "sold": 12131,
                    "sales": 21213414,
                }

                new_data.append(data)

        return Response({"category name": new_data})


class WholesellerDashboardSubCategoriesViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        wholeseller_queryset = Wholeseller.objects.filter(id=pk)
        data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
        subcategory_names = []
        new_data = []
        for bazaar_id in data:
            product_queryset = Product.objects.filter(bazaar=bazaar_id)
            for product in product_queryset:
                data = {
                    "subcategory_name": product.subcategory.subcategory_name,
                    "most_purchased_by": "abc limited",
                    "sold": 12131,
                    "sales": 21213414,
                }

                new_data.append(data)

        return Response({"subcategory name": new_data})


class WholesellerDashboardAdsPerformanceViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        data = Ads.objects.filter(id=pk)
        ad_title = []
        new_data = []
        for id in data:
            data = {
                "Name": id.ad_title,
                "Product": "Mobile",
                "City": "Jaipur",
                "Price": 21213414,
                "Sold": 200,
                "Amount Spend": 1000,
            }

            new_data.append(data)
        return Response({"Ads Performance": new_data})


class WholesellerDashboardTopBranchesViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        data = []
        new_data = []
        data = {
            "Branch Name": "Branch 1",
            "Orders": 1200,
            "Revenue": 100000,
            "State": "Delhi-NCR",
        }
        new_data.append(data)
        return Response({"Top Branches": new_data})


class WholesellerBazaarListViewSet(viewsets.ModelViewSet):
    queryset = Wholeseller.objects.all()
    serializer_class = WholelsellerBazaarListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(id=pk)
        return queryset


class WholesellerBranchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Branch.objects.all()
    serializer_class = WholesellerBranchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]


class WholesellerBazaarProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WholesellerBazaarProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "product_name",
    ]
    filterset_fields = [
        "category_group",
        "category",
        "subcategory",
        "product_brand_name",
        "product_active",
        "product_stocks",

    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        bazaar_id = self.kwargs.get("bazaar_id")
        if pk and bazaar_id:
            queryset = queryset.filter(bazaar__wholeseller__id=pk, bazaar_id=bazaar_id)
        return queryset


class WholesellerBazaarViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WholesellerBazaarSerializer
    queryset = Bazaar.objects.all()

    def get_queryset(self):
        queryset = Bazaar.objects.all()
        bazaar_id = self.kwargs.get("bazaar_id")
        pk = self.kwargs.get("pk")
        if pk and bazaar_id:
            queryset = queryset.filter(wholeseller__id=pk, id=bazaar_id)
        return queryset


# -------------- wholeseller agent
class WholesellerAgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = WholesellerAgent.objects.all().order_by("id")
    serializer_class = WholesellerAgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["wholeseller_agent_name"]
<<<<<<< HEAD
=======


class WholesellerIdAgentViewSet(viewsets.ModelViewSet):
    serializer_class = WholesellerIdAgentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wholeseller_id = self.kwargs['wholeseller_id']
        return WholesellerAgent.objects.filter(wholeseller_id=wholeseller_id)
>>>>>>> 20d834c324aa905461011ab676850730afe67f87


class WholesellerAgentVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        agent_number = request.data.get("wholeseller_agent_number")
        agent_otp = request.data.get("wholeseller_agent_otp")

        try:
            agent = WholesellerAgent.objects.get(wholeseller_agent_number=agent_number)
            if agent.wholeseller_agent_otp == int(agent_otp):
                # OTP is valid
                agent.wholeseller_agent_otp = None
                agent.save(update_fields=["wholeseller_agent_otp"])
                # Get the User object associated with the Agent
                user = agent.wholeseller_agent_user
                access_token = AccessToken.for_user(user)
                access_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=6400)
                )
                refresh_token = RefreshToken.for_user(user)
                refresh_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=166400)
                )
                return Response(
                    {
                        "access_token": str(access_token),
                        "refresh_token": str(refresh_token),
                        "agent_id": agent.id,
                    }
                )
            else:
                status_code = common_status["unauthorized"]["code"]
                payload = {"details": "Invalid OTP."}
                return Response(payload, status=status_code)
        except Agent.DoesNotExist:
            # Agent not found
            payload = {"details": "Agent not found"}
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)


class WholesellerAgentVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        agent_number = data.get("wholeseller_agent_number")
        password = data.get("agent_otp")
        payload = {}
        if agent_number != "":
            agent_otp = random.randrange(000000, 999999)
            try:
                data = WholesellerAgent.objects.get(wholeseller_agent_number=agent_number)
                data.wholeseller_agent_otp = agent_otp
                data.save(update_fields=["wholeseller_agent_otp"])
                if data:
                    user = User.objects.filter(id=data.wholeseller_agent_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": agent_otp,
                            "details": "Agent OTP sent of registered mobile Number",
                        }
                        status_code = common_status["success"]["code"]
                    else:
                        payload = {"details": "No user found for the agent"}
                        status_code = common_status["not_found"]["code"]
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
                    status_code = common_status["not_found"]["code"]

            except Agent.DoesNotExist:
                payload = {"details": "Agent not found"}
                status_code = common_status["unauthorized"]["code"]

        else:
            payload = {"details": "Something went wrong."}
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]

        return Response(payload, status=status_code)


class WholesellerAgentApplicationStatusViews(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        agent_number = request.data.get("agent_number")
        agent_status = request.data.get("agent_status")
        kyc_remarks = request.data.get("kyc_remarks")
        try:
            agent = Agent.objects.get(agent_number=agent_number)
            user = agent.agent_user
            if user is None:
                return Response({"message": "Agent user not found."})

            if agent_status == "CREATED":
                message = f"Your application_id {agent_number} is in process. If you have any Query? Fell free to contact Us ."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif agent_status == "PENDING":
                message = f"Your application_id {agent_number} is in process. we have received your Application, Our team is reviewing it. Thank You for your patience .if you have any Query? Fell free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif agent_status == "KYCREJECTED" and kyc_remarks is not None:
                message = f"Your application_id {agent_number} is rejected ! {kyc_remarks}. If you have any Query? Feel free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif agent_status == "KYCAPPROVED":
                message = f"Your application_id {agent_number} is approved !  If you have any Query? Feel free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            else:
                return Response({"message": "Invalid agent status."})
        except Agent.DoesNotExist:
            return Response({"message": "Agent not found."})
<<<<<<< HEAD
=======


class WholesellerIdAgentViewSetIdViewSet(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, wholeseller_id, agent_id):
        try:
            wholeseller = Wholeseller.objects.get(id=wholeseller_id)
            agent = WholesellerAgent.objects.get(id=agent_id, wholeseller=wholeseller)

            agent_serializer = WholesellerAgentSerializer(agent)

            return Response({
                'agent': agent_serializer.data
            })
        except WholesellerAgent.DoesNotExist:
            return Response({'message': 'Agent not found for the given wholeseller'}, status=404)


# ------------------- wholeseller retailer-------

class RetailerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = WholesellerRetailer.objects.all()
    serializer_class = WholesellerRetailerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wholeseller_retailer_name']


class WholesellerIdRetailerAPIView(views.APIView):
    serializer_class = WholesellerRetailerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, wholeseller_id):
        retailers = WholesellerRetailer.objects.filter(wholeseller_retailer=wholeseller_id)
        serializer = self.serializer_class(retailers, many=True)
        return Response(serializer.data)


class WholesellerIdRetailerIdViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, wholeseller_id, retailer_id):
        try:
            retailer = WholesellerRetailer.objects.get(id=retailer_id, wholeseller_retailer__id=wholeseller_id)
            serializer = WholesellerRetailerSerializer(retailer)
            return Response(serializer.data)
        except WholesellerRetailer.DoesNotExist:
            return Response(status=404)

class WholesellerRetailerVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        retailer_number = request.data.get("wholeseller_retailer_number")
        retailer_otp = request.data.get("wholeseller_retailer_otp")

        try:
            retailer = WholesellerRetailer.objects.get(wholeseller_retailer_number=retailer_number)
            if retailer.wholeseller_retailer_otp == int(retailer_otp):
                # OTP is valid
                retailer.wholeseller_retailer_otp = None
                retailer.save(update_fields=["wholeseller_retailer_otp"])
                # Get the User object associated with the Retailer
                user = retailer.wholeseller_retailer_user
                access_token = AccessToken.for_user(user)
                access_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=6400)
                )
                refresh_token = RefreshToken.for_user(user)
                refresh_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=166400)
                )
                return Response(
                    {
                        "access_token": str(access_token),
                        "refresh_token": str(refresh_token),
                        "retailer_id": retailer.id,
                    }
                )
            else:
                status_code = common_status["unauthorized"]["code"]
                payload = {"details": "Invalid OTP."}
                return Response(payload, status=status_code)
        except Retailer.DoesNotExist:
            # Retailer not found
            payload = {"details": "Retailer not found"}
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)


class WholesellerRetailerVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        retailer_number = data.get("wholeseller_retailer_number")
        password = data.get("wholeseller_retailer_otp")
        payload = {}
        if retailer_number != "":
            retailer_otp = random.randrange(000000, 999999)
            try:
                data = WholesellerRetailer.objects.get(wholeseller_retailer_number=retailer_number)
                data.wholeseller_retailer_otp = retailer_otp
                data.save(update_fields=["wholeseller_retailer_otp"])
                if data:
                    user = User.objects.filter(id=data.wholeseller_retailer_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": retailer_otp,
                            "details": "Retailer OTP sent of registered mobile Number",
                        }
                        status_code = common_status["success"]["code"]
                    else:
                        payload = {"details": "No user found for the retailer"}
                        status_code = common_status["not_found"]["code"]
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
                    status_code = common_status["not_found"]["code"]

            except Retailer.DoesNotExist:
                payload = {"details": "Retailer not found"}
                status_code = common_status["unauthorized"]["code"]

        else:
            payload = {"details": "Something went wrong."}
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]

        return Response(payload, status=status_code)
# --------------------wholeseller branch --------------

class WholesellerBranchAddProduct(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    queryset = Branch_Product.objects.all()
    serializer_class = BranchProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["branch"]

class WholesellerBranchCategoryWisePlanList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Branch_Category_Wise_Plan.objects.all()
    serializer_class = BranchCategoryWisePlanSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["category"]

class WholesellerBranchSubCategoryWisePlanList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Branch_Sub_Category_Wise_Plan.objects.all()
    serializer_class = BranchSubCategoryWisePlanSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ["sub_category"]

class WholesellerBranchItemWisePlanList(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Branch_Item_Wise_Plan.objects.all()
    serializer_class = BranchItemWisePlanSerializer

class WholesellerBranchManagerVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        branch_manager_number = data.get("branch_phone")
        password = data.get("branch_otp")
        payload = {}
        if branch_manager_number != "":
            branch_otp = random.randrange(000000, 999999)
            try:
                data = Branch.objects.get(branch_phone=branch_manager_number)
                data.branch_otp = branch_otp
                data.save(update_fields=["branch_otp"])
                if data:
                    user = User.objects.filter(id=data.wholeseller_branch_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": branch_otp,
                            "details": "Manager's OTP sent of registered mobile Number",
                        }
                        status_code = common_status["success"]["code"]
                    else:
                        payload = {"details": "No user found for the manager"}
                        status_code = common_status["not_found"]["code"]
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
                    status_code = common_status["not_found"]["code"]

            except Retailer.DoesNotExist:
                payload = {"details": "Manager not found"}
                status_code = common_status["unauthorized"]["code"]

        else:
            payload = {"details": "Something went wrong."}
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]

        return Response(payload, status=status_code)


class WholesellerBranchManagerVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        branch_manager_number = request.data.get("branch_phone")
        branch_manager_otp = request.data.get("branch_otp")

        try:
            manager = Branch.objects.get(branch_phone=branch_manager_number)
            if manager.branch_otp == int(branch_manager_otp):
                # OTP is valid
                manager.branch_otp = None
                manager.save(update_fields=["branch_otp"])
                # Get the User object associated with the Retailer
                user = manager.wholeseller_branch_user
                access_token = AccessToken.for_user(user)
                access_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=6400)
                )
                refresh_token = RefreshToken.for_user(user)
                refresh_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=166400)
                )
                return Response(
                    {
                        "access_token": str(access_token),
                        "refresh_token": str(refresh_token),
                        "branch_id": manager.id,
                    }
                )
            else:
                status_code = common_status["unauthorized"]["code"]
                payload = {"details": "Invalid OTP."}
                return Response(payload, status=status_code)
        except Retailer.DoesNotExist:
            # Retailer not found
            payload = {"details": "Manager not found"}
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)


# class BranchProductList(views.APIView):
#     serializer_class = BranchProductSerializer
#     permission_classes = [permissions.AllowAny]
#     authentication_classes = []
#
#     def get(self, request, branch_id):
#         branch = get_object_or_404(Branch, id=branch_id)
#         branch_products = Branch_Product.objects.filter(branch=branch)
#         serializer = self.serializer_class(branch_products, many=True)
#         return Response(serializer.data)
>>>>>>> 20d834c324aa905461011ab676850730afe67f87
