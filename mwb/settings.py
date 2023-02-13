"""
Django settings for mwb project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from datetime import timedelta
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')2$rbl+021dl3a25h4d%8-x5rk0kox+%k!z)mig%gb*9pf483('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True    

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'rest_framework',
    'phonenumber_field',
    'bazaarApp',
    'agentApp',
    'wholesellerApp',
    'parentCategoryApp',
    'categoryApp',
    'subCategoryApp',
    'productApp',
    # 'leaflet',

    # 'corsheaders',
    # 'fcm_django',
    # 'bucket',
    # 'invoice',
    # 'item',
    # 'itemmaster',
    # 'locality',
    # 'order',
    # 'account',
    # 'subcategory',
    # 'dashboard'
]

#custom entry
SITE_ID = 1
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=15),
#     'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=15),
# }


CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'mwb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mwb.wsgi.application'



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mwb',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
    

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

ADMIN_SITE_HEADER = "mwb"


...

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=90),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=95),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=90),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=95),
}


# FCM_DJANGO_SETTINGS = {
#         "FCM_SERVER_KEY": "AAAAHivo2Hg:APA91bEV6kRrACq-unVONzQQ59gX7Ei3VXLq_1Yp23BSInakTY3jRj21Yz8vYHbqI2yOzDMrTQJhJ9wX6B8ZWsb2ZIwj1eGOmOY6giOMTwm5VeHziY5BvbXege9BRrunxjsBj_lHwuZW"
# }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators


# DEFAULT_ITEM_MASTER = 1

# USER_TYPE = (
#     ('C', 'Customer'),
#     ('V', 'Vendor'),
#     ('A', 'Admin')
# )




# MEASUREMENT = (
#     ('Kg', 'Kilogram'),
#     ('Grm', 'Grams'),
#     ('Dzn', 'Dozen'),
#     ('Box', 'Box'),
#     ('Unit', 'Unit'),
#     ('Pack', 'Pack'),
#     ('50g', '50 grams'),
#     ('100g', '100 grams'),
#     ('150g', '150 grams'),
#     ('250g', '250 grams'),
#     ('325g', '325 grams'),
#     ('400g', '400 grams'),
#     ('415g', '415 grams'),
#     ('420g', '420 grams'),
#     ('450g', '450 grams'),
#     ('500g', '500 grams'),
#     ('900g', '900 grams'),
#     ('1200g', '1200 grams'),
#     ('1kg', '1kg'),
#     ('2kg', '2kg'),
#     ('3kg', '3kg'),
#     ('4kg', '4kg'),
#     ('5kg', '5kg'),
#     ('6kg', '6kg'),
#     ('7kg', '7kg'),
#     ('8kg', '8kg'),
#     ('9kg', '9kg'),
#     ('10kg', '10kg'),
#     ('15kg', '15kg'),
#     ('20kg', '20kg'),
#     ('25kg', '25kg'),
#     ('Bunch', 'Bunch'),
#     ('Dozen', 'Dozen'),
#     ('Box', 'Box'),
#     ('Pack', 'Pack'),
#     ('Unit', 'Unit'),
#     ('2pc', '2 pc'),
#     ('3pc', '3 pc'),
#     ('4pc', '4 pc'),
#     ('5pc', '5 pc'),
#     ('6pc', '6 pc'),
#     ('1L', '1 Litre'),
#     ('500ml', '500 ml'),

# )

# # IF update key need to update notification utils as well
# ORDER_STATUS = (
#     ('Pe', 'Confirmed'),
#     ('Pa', 'Packed'),
#     ('Di', 'Dispatched'),
#     ('De', 'Delivered'),
#     ('Ca', 'Cancelled')
# )

# #Customer name / Vendor name / Order Id / Order total
# ORDER_PE_PUSH_TITLE = '🥳 Your order is placed successfully!'
# ORDER_PE_PUSH_TEXT = '\nHey {},\nThe Sabzzy vendor {} has been notified about your order no {} of Rs.{}.\nYour order will be processed shortly.\n\n🍒 Cheers! \nTeam Sabzzy'

# ORDER_PE_PUSH_UNV_TEXT = '\nHey {},\nThe Sabzzy vendor {} has been notified about your order no {}.\nYour order will be processed shortly.\n\n🍒 Cheers! \nTeam Sabzzy'



# ORDER_GEN_PUSH_TITLE = '{} Your order no {} has been {}!'
# ORDER_GEN_PUSH_TEXT = '\nHey {},\nYour order will be {} by {} shortly.\n\n🍒 Cheers! \nTeam Sabzzy'

# ORDER_DE_PUSH_TITLE = '🛍️  Your order no {} has been {}!'
# ORDER_DE_PUSH_TEXT = '\nHey {},\nHope you had a good experience with {}.\nThanks for shopping on Sabzzy App!.\n\n🍒 Cheers! \nTeam Sabzzy'

# ORDER_CA_PUSH_TITLE = '🚫 Your order no {} has been cancelled.'
# ORDER_CA_PUSH_TEXT = '\nHey {},\nYour order has been cancelled by {} due to unavoidable reasons.\nWe regret the inconvenience caused to you.\n\nTeam Sabzzy'


# INVOICE_STATUS = (
#     ('Pa', 'Paid'),
#     ('Po', 'Payment Processed'),
#     ('Un', 'Un-Paid')
# )

# VENDOR_TYPE = (
#     ('Fr', 'Fruits'),
#     ('Ve', 'Vegetables'),
#     ('Bo', 'Fruits & Vegetables'),
#     ('Ms' , 'Meat & Seafood'),
#     ('Ff' , 'Frozen Foods'),
#     ('Db', 'Dairy & Bakery'),
#     ('Ts', 'Tiffin Services')
# )

# SEND_ORDER_NOTIFICATION = (
#     ('Ninad', '8601343535'),
# )


# PAYMENT_OPTION = (
#     ('GP', 'Gpay'),
#     ('PP', 'Phonepay'),
#     ('BH', 'Bhim'),
#     ('PT' , 'PayTm'),
#     ('RP', 'RazorPay'),
#     ('Co' , 'COD')
# )

# # leaflet Module
# LEAFLET_CONFIG = {
#     'DEFAULT_CENTER': (6.0, 45.0),
#     'DEFAULT_ZOOM': 5,
#     'MAX_ZOOM': 20,
#     'SCALE': 'imperial'
# }

# # Rest Permission


# STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static") 

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# DATA_UPLOAD_MAX_NUMBER_FIELDS = None 

# SMS_BASE_URL = 'http://enterprise.smsgupshup.com/GatewayAPI/rest'
# LOGIN_SMS_TEMPLATE_ID = '975736'
# #975736 = Prod
# ORDER_SMS_TEMPLATE_ID = '982570'
# ORDER_UAV_SMS_TEMPLATE_ID = '982570'
# SMS_PLATEFORM_USER_ID = '2000192085'
# SMS_PLATEFORM_PASSWORD = '9920933990@Sabzzy'
# SMS_MASK = 'Sabzzy'

#local_settings
try:
    from .local_settings import *
except ImportError as e:
    pass
