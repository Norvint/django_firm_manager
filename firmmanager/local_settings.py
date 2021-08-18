import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCAL_KEY = '8^%-_e1b^7+egl10cu%bs3-&jzj6&x+xg6oj4_3$8y*5utahqk'
LOCAL_ALLOWED_HOSTS = []

LOCAL_DATABASE = {
   'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': 'postgres',
    'HOST': 'localhost',
    'PORT': '5432',
}
