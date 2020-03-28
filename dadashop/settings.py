"""
Django settings for dadashop project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uf8du4bg&^#z6^u(-4j)3za9yft+b3x_gep3$tfa!3do@lmny&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'user',
    'dtoken',
    'goods',
    'carts',
    'orders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dadashop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'dadashop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dadashop',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
            )
CORS_ALLOW_HEADERS = (
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
			)

JWT_TOKEN_KEY = '123456'


# 发邮件配置流程
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
# 固定写法
EMAIL_HOST = 'smtp.qq.com' # 腾讯QQ邮箱 SMTP 服务器地址
EMAIL_PORT = 25
# SMTP服务的端口号
EMAIL_HOST_USER = '564521499@qq.com'
# 发送邮件的QQ邮箱
EMAIL_HOST_PASSWORD = 'xlpcmcpnawipbffg'
# 在QQ邮箱->设置->帐户->“POP3/IMAP......服务” 里得到的在第三方登录QQ邮箱授权码
EMAIL_USE_TLS = False
# 与SMTP服务器通信时,是否启动TLS链接(安全链接)默认false

APPEND_SLASH = False


WEIBO_CLIENT_ID='3844497818'
WEIBO_CLIENT_SECRET='9672085cae07a59b1e137372f9d3fd4a'
WEIBO_REDIRECT_URI='http://127.0.0.1:7000/dadashop/templates/callback.html'



# 写入缓存
CACHES = {
    'default':{'BACKEND':'django_redis.cache.RedisCache',
             'LOCATION':'redis://@127.0.0.1:6379/1',
             'OPTIONS':{'CLIENT_CLASS':'django_redis.client.DefaultClient'}},

    'goods':{'BACKEND':'django_redis.cache.RedisCache',
             'LOCATION':'redis://@127.0.0.1:6379/5',
             'OPTIONS':{'CLIENT_CLASS':'django_redis.client.DefaultClient'}},

    'carts':{'BACKEND':'django_redis.cache.RedisCache',
             'LOCATION':'redis://@127.0.0.1:6379/5',
             'OPTIONS':{'CLIENT_CLASS':'django_redis.client.DefaultClient'}},

}

# 上传图片相关配置
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

MEDIA_URL = '/media/'

PIC_URL = 'http://127.0.0.1:8000' + MEDIA_URL