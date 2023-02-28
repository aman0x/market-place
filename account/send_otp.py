import requests
import random
from django.conf import settings


def send_otp_phone(phone):
    try:
        otp=random.randint(1000,999)
        url=f'https://2factor.in/API/V1/{settings.API_Key}/SMS/{phone}/{otp}'
        response=requests.get(url)
        return otp

    except Exception as e:
        return None

