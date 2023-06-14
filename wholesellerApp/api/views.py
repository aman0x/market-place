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
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.db.models import Q
from retailerApp.models import Retailer

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

        return Response({"Total Products": count})


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


# class WholesellerBazaarListViewSet(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, pk):
#         wholeseller_queryset = Wholeseller.objects.filter(id=pk)
#         data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
#         print(data)
#         new_data = []
#         for bazaar_id in data:
#             Bazaar_queryset = Bazaar.objects.filter(id=bazaar_id[0])
#             print(Bazaar_queryset)
#             for id in Bazaar_queryset:
#                 data = {
#                     "Bazaar id": id.id,
#                     "Bazaar Name": id.bazaar_name
#                 }
#                 new_data.append(data)
#         return Response({"Bazaar List": new_data})

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
        pk= self.kwargs.get("pk")
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
    search_fields = ["agent_name"]


# class WholesellerAgentCommisionRedeemViewset(viewsets.ModelViewSet):
#     queryset = ManageCommision.objects.all().order_by('id')
#     serializer_class = AgentManageCommisionSerializer
#     permission_classes = [permissions.IsAuthenticated]


class WholesellerAgentCommisionRedeemViewset(viewsets.ModelViewSet):
    queryset = WholesellerAgentCommisionRedeem.objects.all().order_by("id")
    serializer_class = WholesellerAgentCommisionRedeemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["id"]


class WholesellerAgentWallet(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, pk):
        data = {
            "total_amount_earned": 1000,
            "total_amount_withdrawn": 500,
            "agent_balance": 700,
            "agent_withdrawable_balance": 200,
        }
        serializer = AgentWalletSerializer(data=data)
        deserialized_data = ""
        try:
            agent = Agent.objects.get(id=pk)
            if agent:
                if serializer.is_valid():
                    deserialized_data = serializer.validated_data
                    return Response(deserialized_data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        deserialized_data, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response("Agent is not valid")
        except:
            return Response("Agent is not available")


class WholesellerAgentVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        agent_number = request.data.get("agent_number")
        agent_otp = request.data.get("agent_otp")

        try:
            agent = Agent.objects.get(agent_number=agent_number)
            if agent.agent_otp == int(agent_otp):
                # OTP is valid
                agent.agent_otp = None
                agent.save(update_fields=["agent_otp"])
                # Get the User object associated with the Agent
                user = agent.agent_user
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
        agent_number = data.get("agent_number")
        password = data.get("agent_otp")
        payload = {}
        if agent_number != "":
            agent_otp = random.randrange(000000, 999999)
            try:
                data = Agent.objects.get(agent_number=agent_number)
                data.agent_otp = agent_otp
                data.save(update_fields=["agent_otp"])
                if data:
                    user = User.objects.filter(id=data.agent_user_id).distinct().first()
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


class WholesellerReportPlanExpireView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        base_url = request.build_absolute_uri('/')
        wholesalers = Wholeseller.objects.filter(wholeseller_agent_id=pk)
        wholeseller_list = []
        for wholeseller in wholesalers:
            today = datetime.now().date()
            try:
                end_date = wholeseller.wholeseller_plan.end_date
            except:
                end_date = None
            try:
                days_left = (end_date - today).days
            except:
                days_left = None
            try:
                wholeseller_image = str(wholeseller.wholeseller_image)
                if wholeseller_image:
                    wholeseller_image = base_url + wholeseller_image
                elif wholeseller_image == "":
                    wholeseller_image = "Image not found"
            except:
                wholeseller_image = "Image not found"

            status = "active"  # default value
            message = "Your plan is active."  # default value
            days = 0

            wholeseller_data = {
                "wholeseller_name": wholeseller.wholeseller_name,
                "wholeseller_image": wholeseller_image,
                "message": message,
                "status": status,
                "days": days,
            }

            if end_date == None:
                message = "No active plan! Please activate"
                status = "No Plan"
                days = "Not Applicable"

            elif days_left <= 0:
                message = "Your plan has expired. Please renew your plan."
                status = "expired"
                days = f"expired by {abs(days_left)} days"

            elif days_left <= 15:
                message = f"Your plan will expiring soon. Please renew soon."
                status = "expiring_soon"
                days = f"expiring in {abs(days_left)} days"

            elif days_left <= 30:
                message = f"Your plan will expire . Please renew soon."
                status = "expiring_soon"
                days = f"expiring in {abs(days_left)} days"

            wholeseller_data["message"] = message
            wholeseller_data["status"] = status
            wholeseller_data["days"] = days

            wholeseller_list.append(wholeseller_data)

        data = {"count": len(wholeseller_list), "wholesellers": wholeseller_list}
        return Response(data)


class WholesellerCountView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get_week_number(self, year, month, day):
        date_obj = date(int(year), int(month), int(day))
        week_number = (date_obj.day - 1) // 7 + 1
        return week_number

    def get_week_of_year(self, year, month, week_of_month):
        first_day_of_month = date(year, month, 1)
        first_week_of_month = first_day_of_month.isocalendar()[1]
        week_of_year = first_week_of_month + week_of_month - 1
        return week_of_year

    def get(self, request, pk):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        week = request.query_params.get("week")
        wholeseller_agent = pk

        qs = Wholeseller.objects.filter(wholeseller_agent=wholeseller_agent)

        if year:
            qs = qs.filter(created_at__year=year)
        if month:
            try:
                month_num = int(month)
                qs = qs.filter(created_at__month=month_num)
            except ValueError:
                qs = qs.filter(created_at__year=year)
        if week:
            try:
                year = int(year)
                month_num = int(month)
                week_of_month = int(week)
                week_of_year = self.get_week_of_year(year, month_num, week_of_month)
                qs = qs.filter(created_at__week=week_of_year)
            except ValueError:
                if year and month:
                    qs = qs.filter(created_at__year=year, created_at__month=month_num)
                else:
                    qs = qs.filter(created_at__year=year)

        month_names = settings.MONTH_NAMES
        # yearly_counts = (
        #     qs.annotate(year=ExtractYear("created_at"))
        #     .values("year")
        #     .annotate(count=Count("id"))
        # )
        # yearly_result = []
        # for item in yearly_counts:
        #     year_num = item["year"]
        #     count = item["count"]
        #     yearly_result.append({"year": year_num, "count": count})

        # monthly_counts = (
        #     qs.annotate(
        #         year=ExtractYear("created_at"), month=ExtractMonth("created_at")
        #     )
        #     .values("year", "month")
        #     .annotate(count=Count("id"))
        # )
        # monthly_result = []
        # for item in monthly_counts:
        #     year_num = item["year"]
        #     month_num = item["month"]
        #     try:
        #         month_name = month_names[month_num]
        #     except (KeyError, TypeError):
        #         month_name = None
        #     count = item["count"]
        #     monthly_result.append(
        #         {"year": year_num, "month": month_name, "count": count}
        #     )

        week_counts = (
            qs.annotate(day=ExtractDay("created_at"), year=ExtractYear("created_at"), month=ExtractMonth("created_at"))
            .values("day", "year", "month")
            .annotate(count=Count("id"))
        )

        week_result = []
        for item in week_counts:
            year_num = item["year"]
            month_num = item["month"]
            day_num = item["day"]
            week_num = self.get_week_number(year_num, month_num, day_num)
            try:
                month_name = month_names[month_num]
            except (KeyError, TypeError):
                month_name = None
            week_name = "Week " + str(week_num)
            count = item["count"]
            week_result.append({"year": year_num, "month": month_name, "week": week_name, "count": count})

        data = {
            "total_wholeseller_count": qs.count(),
            # "no of wholeseller by year": yearly_result,
            # "no of wholeseller by months": monthly_result,
            "Wholesellers": week_result,
        }

        return Response(data)


class WholesellerListViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wholeseller.objects.all().order_by("id")
    serializer_class = WholsellerListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["wholeseller_bazaar", "wholeseller_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(wholeseller_agent=pk)
        return queryset


class WholesellerAgentEarningAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        week = request.query_params.get("week")

        try:
            total_wholesellers_added = Wholeseller.objects.filter(wholeseller_agent=pk)

            # Filter by year
            if year:
                total_wholesellers_added = total_wholesellers_added.filter(
                    created_at__year=year
                )

            # Filter by month
            if month:
                total_wholesellers_added = total_wholesellers_added.filter(
                    created_at__month=month
                )

            # Filter by week
            if week:
                start_date = timezone.now().date() - timedelta(
                    weeks=52
                )  # consider only past 52 weeks
                total_wholesellers_added = total_wholesellers_added.filter(
                    created_at__range=[start_date, timezone.now().date()]
                ).annotate(
                    week_num=Count("id", filter=(models.Q(created_at__week=week)))
                )

            count = total_wholesellers_added.count()
            if count > 0:
                total_commission = 0
                for wholeseller in total_wholesellers_added:
                    if wholeseller.wholeseller_plan:
                        total_commission += wholeseller.wholeseller_plan.amount

                response_data = {
                    "total_wholesellers_added": count,
                    "total_commission": total_commission,
                }

            else:
                response_data = {"message": "No data available for this agent."}

        except Agent.DoesNotExist:
            response_data = {"message": "No data available for this agent."}

        return Response(response_data)


#------------------------- wholeseller retailer

class WholesellerRetailerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Retailer.objects.all()
    serializer_class = WholesellerRetailerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wholeseller_retailer_name']

