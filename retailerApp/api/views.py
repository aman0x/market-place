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
from wholesellerApp.api.serializers import OfferDetailsSerializer
from rest_framework.generics import get_object_or_404
from django.http import Http404
from django.db.models import Sum, F, ExpressionWrapper, FloatField, Count
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
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
            retailer_otp = random.randint(100000, 999999)
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
                    subcart_item.qty = qty
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


class subcart_retailer(viewsets.ModelViewSet):
    serializer_class = SubCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = SubCart.objects.filter(retailer_id=retailer_id, used_in_cart=False)
        return queryset


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wholeseller_id']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# class AllProductByWholesellerId(viewsets.ModelViewSet):
#     serializer_class = ProductWithOfferSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         wholeseller_id = self.kwargs.get('wholeseller_id')
#         wholeseller = get_object_or_404(Wholeseller, pk=wholeseller_id)
#         bazaar_id = wholeseller.wholeseller_bazaar.first().id
#         return Product.objects.filter(bazaar_id=bazaar_id)


class ProductFilterAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductWithOfferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bazaar','category_group','category','subcategory']


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
    serializer_class = OfferDetailsSerializer

    def get_queryset(self):
        queryset = Offers.objects.all().order_by('id')
        wholeseller_id = self.kwargs.get('wholeseller_id')
        if wholeseller_id:
            queryset = queryset.filter(wholeseller_id=wholeseller_id)

        if not queryset.exists():
            raise Response(f"No offers found for the given wholeseller.")

        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        modified_offer_list = []

        for offer in serializer.data:
            product_details = offer['productIdetails']
            offer_discounted_price = float(offer['offer_discounted_price'])
            product_selling_price = float(product_details['product_selling_price'])

            # Calculate the discount percentage
            discount_percentage = round(((product_selling_price - offer_discounted_price) / product_selling_price) * 100)

            modified_offer = {
                **offer,  # Include all original fields from the serializer data
                'discount_percentage': discount_percentage,
            }

            modified_offer_list.append(modified_offer)

        response_data = {
            'results': modified_offer_list,
        }

        return Response(response_data)


class recent_order(viewsets.ModelViewSet):
    serializer_class = RecentProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = SubCart.objects.filter(retailer_id=retailer_id, used_in_cart=True)
        return queryset


class completed_order(viewsets.ModelViewSet):
    serializer_class = CartDetailedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status='SUCCESS',payment_status = 'COMPLETED' ).distinct()
        return queryset


class pending_order(viewsets.ModelViewSet):
    serializer_class = CartDetailedSerializer
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
    serializer_class = CartDetailedSerializer
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
        out_for_delivery_orders = queryset.filter(order_status="OUT_FOR_DELIVERY").count()
        accepted_orders = queryset.filter(order_status="APPROVED").count()
        rejected_orders = queryset.filter(order_status="REJECTED").count()
        success_orders = queryset.filter(order_status="SUCCESS").count()

        data = {
            'total_orders': total_orders,
            'total_values': total_values,
            'pending_orders': pending_orders,
            'out_for_delivery_orders': out_for_delivery_orders,
            'accepted_orders': accepted_orders,
            'rejected_orders': rejected_orders,
            'success_orders': success_orders,
        }

        return Response(data, status=status.HTTP_200_OK)


class report_orders_cart(viewsets.ModelViewSet):
    serializer_class = CartDetailedSerializer
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

        elif payment_type == 'CASH':
            queryset = queryset.filter(payment_type__in=['CASH','UPI', 'CHEQUE', 'NEFT/RTGS'])
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
            queryset = queryset.filter(carts__order_created_at__year=year_filter)

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        subcart_serializer = self.serializer_class(queryset, many=True)

        product_details = []
        total_values = sum(subcart.get('total_price', 0) for subcart in subcart_serializer.data)

        for subcart_data in subcart_serializer.data:
            product_id = subcart_data['product']
            product_qty = subcart_data['qty']
            product_total_value = subcart_data['total_price']

            product = get_object_or_404(Product, pk=product_id)

            product_percentage = (product_total_value / total_values) * 100

            product_info = {
                'product_name': product.product_name,
                'category': product.category.category_name,
                'subcategory': product.subcategory.subcategory_name,
                'quantity': product_qty,
                'total_value': product_total_value,
                'product_percentage': product_percentage,
                'product_photo': product.product_upload_front_image.url if product.product_upload_front_image else None,
            }

            product_details.append(product_info)

        data = {
            'products': product_details,
        }
        return Response(data, status=status.HTTP_200_OK)


class report_products_top_category(viewsets.ModelViewSet):
    serializer_class = SubCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)

        queryset = SubCart.objects.filter(retailer=retailer_id, used_in_cart=True)

        if year_filter:
            queryset = queryset.filter(carts__order_created_at__year=year_filter)

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        subcart_serializer = self.serializer_class(queryset, many=True)

        category_details = {}
        total_values = sum(subcart.get('total_price', 0) for subcart in subcart_serializer.data)

        for subcart_data in subcart_serializer.data:
            product_id = subcart_data['product']
            product_qty = subcart_data['qty']
            product_total_value = subcart_data['total_price']

            if product_id:
                product = get_object_or_404(Product, pk=product_id)
                category = product.category

                category_name = category.category_name
                category_image = category.category_ref_image.url if category.category_ref_image else None

                product_percentage = (product_total_value / total_values) * 100

                if category_name not in category_details:
                    category_details[category_name] = {
                        'category_name': category_name,
                        'category_image': category_image,
                        'total_quantity': product_qty,
                        'total_value': product_total_value,
                        'category_percentage': product_percentage,
                    }
                else:
                    # If category_name is already present, increase the quantity and total value
                    category_details[category_name]['total_quantity'] += product_qty
                    category_details[category_name]['total_value'] += product_total_value

            categories_list = list(category_details.values())

            data = {
                'categories': categories_list,
            }
            return Response(data, status=status.HTTP_200_OK)


class report_products_top_sub_category(viewsets.ModelViewSet):
    serializer_class = SubCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)

        queryset = SubCart.objects.filter(retailer=retailer_id, used_in_cart=True)

        if year_filter:
            queryset = queryset.filter(carts__order_created_at__year=year_filter)

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        subcart_serializer = self.serializer_class(queryset, many=True)
        total_values = sum(subcart.get('total_price', 0) for subcart in subcart_serializer.data)

        subcategory_details = {}

        for subcart_data in subcart_serializer.data:
            product_id = subcart_data['product']
            product_qty = subcart_data['qty']
            product_total_value = subcart_data['total_price']

            if product_id:
                product = get_object_or_404(Product, pk=product_id)
                subcategory = product.subcategory

                subcategory_name = subcategory.subcategory_name
                subcategory_image = subcategory.subcategory_ref_image.url if subcategory.subcategory_ref_image else None

                product_percentage = (product_total_value / total_values) * 100

                if subcategory_name not in subcategory_details:
                    subcategory_details[subcategory_name] = {
                        'subcategory_name': subcategory_name,
                        'subcategory_image': subcategory_image,
                        'total_quantity': product_qty,
                        'total_value': product_total_value,
                        'subcategory_percentage': product_percentage,
                    }
                else:
                    # If subcategory_name is already present, increase the quantity and total value
                    subcategory_details[subcategory_name]['total_quantity'] += product_qty
                    subcategory_details[subcategory_name]['total_value'] += product_total_value

        subcategories_list = list(subcategory_details.values())

        data = {
            'subcategories': subcategories_list,
        }
        return Response(data, status=status.HTTP_200_OK)


class report_payment(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)
        payment_type = self.request.query_params.get('payment_type','').upper()

        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id)

        if year_filter:
            queryset = queryset.filter(order_created_at__year=year_filter)

        if payment_type == 'CREDIT':
            queryset = queryset.filter(payment_type='CREDIT')

        elif payment_type == 'CASH':
            queryset = queryset.filter(payment_type__in=['CASH', 'UPI', 'CHEQUE', 'NEFT/RTGS'])

        queryset = queryset.distinct()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Calculate total amounts for cash and credit payments
        cash_total = queryset.filter(payment_type__in = ['CASH','UPI', 'CHEQUE', 'NEFT/RTGS'], order_status='SUCCESS', payment_status='COMPLETED').aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
        credit_total = queryset.filter(payment_type='CREDIT', order_status='SUCCESS', payment_status='COMPLETED').aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0

        # Calculate total amounts for pending cash and credit payments
        pending_cash_total = queryset.filter(payment_type__in=['CASH','UPI', 'CHEQUE', 'NEFT/RTGS'], order_status='PENDING').aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
        pending_credit_total = queryset.filter(payment_type='CREDIT', order_status='PENDING').aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0

        # Calculate total amount paid (cash + credit) and total amount pending (pending cash + pending credit)
        total_paid = cash_total + credit_total
        total_pending = pending_cash_total + pending_credit_total

        successful_payments = queryset.filter(payment_status='COMPLETED', order_status='SUCCESS').values('payment_date', 'payment_type', 'payment_amount')
        data = {
            'total_paid': total_paid,
            'cash_total': cash_total,
            'credit_total': credit_total,
            'total_pending': total_pending,
            'pending_cash_total': pending_cash_total,
            'pending_credit_total': pending_credit_total,
            'successful_payments': successful_payments,
        }

        return Response(data, status=status.HTTP_200_OK)


class my_performance(viewsets.ModelViewSet):
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
        retailer_qsets = Retailer.objects.filter(id=self.kwargs.get('retailer_id')).distinct()
        cart_qsets = Cart.objects.filter(cart_items__retailer_id=self.kwargs.get('retailer_id'), order_status="SUCCESS",payment_type="CREDIT").distinct()

        num_orders = queryset.count()
        total_amount_spent = queryset.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
        credit_allowed_bills = retailer_qsets.aggregate(Sum('retailer_no_of_bills_allowed'))['retailer_no_of_bills_allowed__sum'] or 0
        credit_limit = retailer_qsets.aggregate(Sum('retailer_credit_limit'))['retailer_credit_limit__sum'] or 0
        credit_amount = retailer_qsets.aggregate(Sum('retailer_credit_amount'))['retailer_credit_amount__sum'] or 0
        used_credit_amount = cart_qsets.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0
        used_allowed_bills = cart_qsets.count()
        data = {
            'number_of_orders': num_orders,
            'amount_spent': total_amount_spent,
            'allowed_bills': credit_allowed_bills,
            'remaining_allowed_bills': credit_allowed_bills - used_allowed_bills,
            'credit_limit': credit_limit,
            'available_credit_amount': credit_amount - used_credit_amount,
            'credit_days': 10,
            'used_allowed_bills': used_allowed_bills,
            'used_credit_days': 10,
        }
        return Response(data, status=status.HTTP_200_OK)


class my_performance_order(viewsets.ModelViewSet):
    serializer_class = MyPerformanceOrder
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)
        payment_type = self.request.query_params.get('payment_type', '').upper()

        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status="SUCCESS")
        if year_filter:
            queryset = queryset.filter(order_created_at__year=year_filter)

        if payment_type == "CREDIT":
            queryset = queryset.filter(payment_type=payment_type)
        elif payment_type == "CASH":
            queryset = queryset.filter(payment_type__in=['CASH', 'UPI', 'CHEQUE', 'NEFT/RTGS'])
        else:
            return queryset.distinct()
        return queryset.distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class my_transactions(viewsets.ModelViewSet):
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

        # Calculate total_amount_spent
        total_amount_spent = queryset.aggregate(Sum('payment_amount'))['payment_amount__sum'] or 0

        # Calculate order_amount
        order_amount_expression = ExpressionWrapper(
            Sum(F('cart_items__product__product_selling_price') * F('cart_items__qty')),
            output_field=FloatField()
        )
        order_amount = total_amount_spent - queryset.aggregate(order_amount=order_amount_expression)['order_amount']

        # Calculate advanced_amount and pending_amount
        if order_amount > 0:
            advanced_amount = order_amount
            pending_amount = 0
        else:
            pending_amount = -order_amount
            advanced_amount = 0

        # Include additional fields for each cart
        cart_data = []
        for cart in queryset:
            cart_total_value = 0
            for cart_item in cart.cart_items.all():
                cart_total_value += cart_item.qty * cart_item.product.product_selling_price

            cart_info = {
                'transaction_id': cart.pk,
                'amount_paid': cart.payment_amount,
                'payment_type': cart.payment_type,
                'payment_date': cart.payment_date,
                'order_id': cart.order_id,
                'advanced_paid_amount': cart.payment_amount - cart_total_value if (cart.payment_amount - cart_total_value) > 0 else 0,
                'total_value': cart_total_value,

                # Include any other relevant fields here
            }
            cart_data.append(cart_info)

        response_data = {
            'total_amount_spent': total_amount_spent,
            'advanced_amount': advanced_amount,
            'pending_amount': pending_amount,
            'transactions': cart_data
        }

        return Response(response_data)


class credit_orders_details(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        year_filter = self.request.query_params.get('year', None)
        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status="SUCCESS", payment_type="CREDIT")
        if year_filter:
            queryset = queryset.filter(order_created_at__year=year_filter)
        queryset = queryset.distinct()
        return queryset


class WholesellerOrders(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wholeseller_id = self.kwargs.get('wholeseller_id')
        queryset = Cart.objects.filter(cart_items__wholeseller_id=wholeseller_id).distinct()
        return queryset


class OutForDeliveryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OutForDeliverySerializer

    def get_queryset(self):
        wholeseller_id = self.kwargs.get('wholeseller_id')
        retailer_id = self.kwargs.get('retailer_id')

        queryset = OutForDelivery.objects.all().order_by('id')

        if retailer_id and not wholeseller_id:
            queryset = OutForDelivery.objects.filter(retailer_id=retailer_id).distinct()

        if not retailer_id and wholeseller_id:
            queryset = OutForDelivery.objects.filter(wholeseller_id=wholeseller_id).distinct()

        if retailer_id and wholeseller_id:
            queryset = OutForDelivery.objects.filter(wholeseller_id=wholeseller_id, retailer_id=retailer_id).distinct()

        if queryset:
            return queryset
        else: return Response({data:"no data found"})


class OrderStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderStatusSerializer

    def get_queryset(self):
        wholeseller_id = self.kwargs.get('wholeseller_id')
        retailer_id = self.kwargs.get('retailer_id')

        queryset = OrderStatus.objects.all().order_by('id')
        if retailer_id and not wholeseller_id:
            queryset = OrderStatus.objects.filter(retailer_id=retailer_id).distinct()

        if not retailer_id and wholeseller_id:
            queryset = OrderStatus.objects.filter(wholeseller_id=wholeseller_id).distinct()

        if retailer_id and wholeseller_id:
            queryset = OrderStatus.objects.filter(wholeseller_id=wholeseller_id, retailer_id=retailer_id).distinct()

        if queryset:
            return queryset
        else:
            data = {'data': 'no data found'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class PaymentDetailsView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        retailer_id = self.kwargs.get('retailer_id')
        payment_status = self.request.query_params.get('payment_status', 'PENDING').upper()
        queryset = Cart.objects.filter(cart_items__retailer_id=retailer_id, order_status="SUCCESS",)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        queryset = queryset.distinct()
        return queryset

