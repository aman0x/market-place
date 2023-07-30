from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import *
from retailerApp.models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from datetime import timedelta, datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
import random
from rest_framework import filters, status
from django.core.exceptions import ValidationError
from categoryApp.api.serializers import CategorySerializer
from categoryApp.models import Category
from productApp.api.serializers import ProductSerializer
from wholesellerApp.models import Offers
from wholesellerApp.api.serializers import OfferSerializer
from rest_framework.generics import get_object_or_404
from django.http import Http404
from django.db.models import Sum, Count
from rest_framework.decorators import action
common_status = settings.COMMON_STATUS


class RetailerViewSet(viewsets.ModelViewSet):
    serializer_class = RetailerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["retailer_name"]

    def get_queryset(self):
        queryset = Retailer.objects.all().order_by('id')

        state_id = self.request.query_params.get('state_id')
        district_id = self.request.query_params.get('district_id')
        city_id = self.request.query_params.get('city_id')
        retailer_type = self.request.query_params.get('retailer_type_id')
        status = self.request.query_params.get('retailer_status')
        agent_type = self.request.query_params.get('retailer_agent_id')
        plan = self.request.query_params.get('plan')

        if state_id:
            queryset = queryset.filter(retailer_state_id=state_id)
        if district_id:
            queryset = queryset.filter(retailer_district_id=district_id)
        if city_id:
            queryset = queryset.filter(retailer_city_id=city_id)
        if retailer_type:
            queryset = queryset.filter(retailer_type_id=retailer_type)
        if status:
            queryset = queryset.filter(retailer_status__icontains=status)
        if agent_type:
            queryset = queryset.filter(retailer_agent_id=agent_type)
        if plan:
            queryset = queryset.filter(retailer_plan_id=plan)

        return queryset


class RetailerVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        retailer_number = data.get("retailer_number")
        password = data.get("retailer_otp")
        payload = {}
        if retailer_number != "":
            retailer_otp = random.randrange(000000, 999999)
            try:
                data = RetailerMobile.objects.get(retailer_number=retailer_number)
                data.retailer_otp = retailer_otp
                data.save(update_fields=["retailer_otp"])
                if data:
                    user = User.objects.filter(id=data.retailer_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": retailer_otp,
                            "details": "retailer OTP sent of registered mobile Number",
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
                payload = {"details": "retailer not found"}
                status_code = common_status["unauthorized"]["code"]

        else:
            payload = {"details": "Something went wrong."}
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]

        return Response(payload, status=status_code)


class RetailerVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        retailer_number = request.data.get("retailer_number")
        retailer_otp = request.data.get("retailer_otp")

        try:
            retailer = RetailerMobile.objects.get(retailer_number=retailer_number)
            if retailer.retailer_otp == int(retailer_otp):
                # OTP is valid
                retailer.retailer_otp = None
                retailer.save(update_fields=["retailer_otp"])
                # Get the User object associated with the retailer
                user = retailer.retailer_user
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
        except retailer.DoesNotExist:
            # retailer not found
            payload = {"details": "retailer not found"}
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)


class SubCartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubCart.objects.all().order_by('id')
    serializer_class = SubCartSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        qty = int(request.data.get("qty"))
        retailer_id = request.data.get("retailer")

        try:
            product = Product.objects.get(pk=product_id)
            retailer = Retailer.objects.get(pk=retailer_id)

            # Check if the SubCart has already been used in a cart
            existing_subcart = SubCart.objects.filter(
                product=product, retailer=retailer, used_in_cart=True
            ).first()

            if existing_subcart:
                subcart_item = SubCart.objects.filter(product=product, retailer=retailer, used_in_cart=False).first()
                if not subcart_item:
                    subcart_item = SubCart.objects.create(product=product, retailer=retailer, qty=qty, used_in_cart=False)
                else:
                    subcart_item.qty += qty
                    subcart_item.save()
            else:
                subcart_item, created = SubCart.objects.get_or_create(
                    product=product,
                    retailer=retailer,
                    defaults={"qty": qty, "used_in_cart": False},
                )

                if not created:
                    # Item already exists, increase the quantity
                    subcart_item.qty += qty
                    subcart_item.save()

            serializer = self.get_serializer(subcart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        except Retailer.DoesNotExist:
            return Response({"error": "Retailer not found."}, status=status.HTTP_404_NOT_FOUND)


class subcart_retailer(viewsets.ModelViewSet):
    serializer_class = SubCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = SubCart.objects.filter(retailer_id=retailer_id, used_in_cart=False)
        return queryset


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all().order_by('id')


class UpdateSubCartUsedInCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            cart_ids = request.data.get('cart_ids', [])  # List of cart IDs
            subcarts_to_update = SubCart.objects.filter(carts__id__in=cart_ids)

            # Update used_in_cart field for SubCart instances present in the specified carts
            for subcart in subcarts_to_update:
                subcart.used_in_cart = True
                subcart.save()

            return Response({"message": "used_in_cart updated for SubCart instances present in the specified carts."},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class cart_retailer(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id).distinct()
        return queryset


class Checkout(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutSerializer
    queryset = Cart.objects.all().order_by("id")

    def perform_create(self, serializer):
        serializer.save()


class WholesellerIdRetailerAPIView(views.APIView):
    serializer_class = WholesellerRetailerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, wholeseller_id):
        retailers = Retailer.objects.filter(retailer_wholeseller=wholeseller_id)
        serializer = self.serializer_class(retailers, many=True)
        return Response(serializer.data)


class WholesellerIdRetailerIdViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, wholeseller_id, retailer_id):
        try:
            retailer = Retailer.objects.get(id=retailer_id, retailer_wholeseller__id=wholeseller_id)
            serializer = WholesellerRetailerSerializer(retailer)
            return Response(serializer.data)
        except Retailer.DoesNotExist:
            return Response(status=404)


class RetailerNotification(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetailerSerializer

    def get_queryset(self):
        if self.request.query_params.get('retailer_number') and not self.request.query_params.get('retailer_wholeseller'):
            retailer_number = None
            try:
                retailer_number = self.request.query_params.get('retailer_number')
                retailer_number = '+' + retailer_number
            except:
                if retailer_number is None:
                    raise ValidationError("Retailer number not provided")

            queryset = Retailer.objects.filter(retailer_number__retailer_number=retailer_number)
            return queryset

        elif self.request.query_params.get('retailer_number') and self.request.query_params.get('retailer_wholeseller'):
                retailer_number = self.request.query_params.get('retailer_number')
                retailer_number = '+' + retailer_number
                retailer_wholeseller = self.request.query_params.get('retailer_wholeseller')
                queryset = Retailer.objects.filter(retailer_number__retailer_number=retailer_number, retailer_wholeseller=retailer_wholeseller)
                return queryset


class RetailerNumberViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetailerNumberSerializer
    queryset = RetailerMobile.objects.all().order_by("id")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        retailer_number = serializer.validated_data.get("retailer_number")

        # Check if retailer number already exists
        existing_retailer = RetailerMobile.objects.filter(retailer_number=retailer_number).first()
        if existing_retailer:
            # Return the existing retailer's ID
            return Response({
                "id": existing_retailer.id,
                "retailer_number": retailer_number
            } , status=status.HTTP_200_OK)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Update only the is_auto_fill field
        serializer.save(is_auto_fill=request.data.get("is_auto_fill", instance.is_auto_fill))

        return Response(serializer.data)


class RetailerDetailsByNumberViewSet(viewsets.ModelViewSet):
    serializer_class = RetailerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["retailer_wholeseller__wholeseller_name"]

    def get_queryset(self):
        retailer_number = self.kwargs['retailer_number']
        retailer_number = '+' + str(retailer_number)
        queryset = Retailer.objects.filter(retailer_number__retailer_number=retailer_number)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RetailerIdWholesellerIdCreateOrderNew(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wholeseller_id = self.kwargs.get('wholeseller_id')
        wholeseller = get_object_or_404(Wholeseller, pk=wholeseller_id)
        bazaar_id = wholeseller.wholeseller_bazaar.first().id
        return Category.objects.filter(bazaar_id=bazaar_id)


class FilterProductByCategory(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, retailer_id, wholeseller_id, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ClickPhotoOrderView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoOrderSerializer
    queryset = PhotoOrder.objects.all().order_by("id")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllProductByWholesellerId(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wholeseller_id = self.kwargs.get('wholeseller_id')
        wholeseller = get_object_or_404(Wholeseller, pk=wholeseller_id)
        bazaar_id = wholeseller.wholeseller_bazaar.first().id
        return Product.objects.filter(bazaar_id=bazaar_id)


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DeliveryAddress.objects.all()
        retailer_id = self.request.query_params.get('retailer_id')
        if retailer_id:
            queryset = queryset.filter(retailer_id=retailer_id)
        return queryset

class RetailerOffer(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OfferSerializer

    def get_queryset(self):
        queryset = Offers.objects.all().order_by('id')
        wholeseller_id = self.kwargs.get('wholeseller_id')
        if wholeseller_id:
            queryset = queryset.filter(wholeseller_id=wholeseller_id)

        if not queryset.exists():
            raise Response(f"No offers found for the given wholeseller.")

        return queryset


class recent_order(viewsets.ModelViewSet):
    serializer_class = RecentProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = SubCart.objects.filter(retailer_id=retailer_id, used_in_cart=True)
        return queryset


class completed_order(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status='SUCCESS',payment_status = 'COMPLETED' ).distinct()
        return queryset


class pending_order(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status='SUCCESS',payment_status = 'PENDING' ).distinct()
        return queryset

class nav_notification(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status= "SUCCESS" ).distinct()
        return queryset


class report_orders(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)

        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status="SUCCESS")

        if year_filter:
            queryset = queryset.filter(order_created_at__year=year_filter)

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_orders = queryset.count()

        # Use serializer method to calculate total value
        total_values = sum(cart.get('total_value', 0) for cart in self.serializer_class(queryset, many=True).data)

        pending_orders = queryset.filter(order_status="PENDING").count()
        accepted_orders = queryset.filter(order_status="APPROVED").count()
        rejected_orders = queryset.filter(order_status="REJECTED").count()
        success_orders = queryset.filter(order_status="SUCCESS").count()


        data = {
            'total_orders': total_orders,
            'total_values': total_values,
            'pending_orders': pending_orders,
            'accepted_orders': accepted_orders,
            'rejected_orders': rejected_orders,
            'success_orders': success_orders,
        }

        return Response(data, status=status.HTTP_200_OK)


class report_orders_cart(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        payment_type = self.request.query_params.get('payment_type', '').upper()
        year_filter = self.request.query_params.get('year', None)

        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id,payment_status='COMPLETED',order_status='SUCCESS')
        queryset = queryset.distinct()

        if year_filter:
            queryset = queryset.filter(order_created_at__year=year_filter)

        if payment_type == 'CREDIT':
            queryset = queryset.filter(payment_type='CREDIT')
        elif payment_type in ['CASH', 'CHEQUE', 'NEFT/RTGS']:
            queryset = queryset.filter(payment_type__in=['CASH', 'CHEQUE', 'NEFT/RTGS'])
        else:
            return queryset

        return queryset


class report_product(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)

        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status="SUCCESS")

        if year_filter:
            queryset = queryset.filter(order_created_at__year=year_filter)

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_values = sum(cart.get('total_value', 0) for cart in self.serializer_class(queryset, many=True).data)
        total_products = queryset.aggregate(Sum('cart_items__qty'))['cart_items__qty__sum'] or 0
        data = {
            'total_values': total_values,
            'total_products': total_products,
        }

        return Response(data, status=status.HTTP_200_OK)


class report_product(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)

        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status="SUCCESS")

        if year_filter:
            queryset = queryset.filter(order_created_at__year=year_filter)

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_values = sum(cart.get('total_value', 0) for cart in self.serializer_class(queryset, many=True).data)
        total_products = queryset.aggregate(Sum('cart_items__qty'))['cart_items__qty__sum'] or 0
        data = {
            'total_values': total_values,
            'total_products': total_products,
        }

        return Response(data, status=status.HTTP_200_OK)


class report_products_top_product(viewsets.ModelViewSet):
    serializer_class = SubCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)

        queryset = SubCart.objects.filter(retailer=retailer_id, used_in_cart=True)

        if year_filter:
            queryset = queryset.filter(cart__order_created_at__year=year_filter)

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Serialize subcart objects to get product details
        subcart_serializer = self.serializer_class(queryset, many=True)

        # Create a dictionary to store product details using the product_id as the key
        product_details = {}

        for subcart_data in subcart_serializer.data:
            product_id = subcart_data['product']
            product_qty = subcart_data['qty']
            product_total_value = subcart_data['total_price']

            if product_id not in product_details:
                # Retrieve the product object from the database
                product = get_object_or_404(Product, pk=product_id)

                # Store product details in the dictionary
                product_details[product_id] = {
                    'product_id': product_id,
                    'product_name': product.product_name,
                    'product_brand_name': product.product_brand_name,
                    'product_description': product.product_description,
                    'category': product.category.category_name,
                    'subcategory': product.subcategory.subcategory_name,
                    'quantity': product_qty,
                    'total_value': product_total_value,
                }
            else:
                # If product_id is already present, increase the quantity and total value
                product_details[product_id]['quantity'] += product_qty
                product_details[product_id]['total_value'] += product_total_value

        # List of product details
        products_list = list(product_details.values())

        data = {
            'products': products_list,
        }
        return Response(data, status=status.HTTP_200_OK)