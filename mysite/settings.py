"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# manage.py 와 django-admin.py의 차이 - https://devlog.jwgo.kr/2018/02/07/what-is-the-diff-btw-manage-django-admin/

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+-m#29!lgboo=^^ayh_lgrc=(9wtz@3_(qiloaa_x2u4c4%l2='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
#앱 - 다른 프로젝트에서 사용할 수 있음
# 장고 인스턴스에서 활성화된 모든 장고 어플리케이션의 이름이 담겨있음.
INSTALLED_APPS = [
    'polls.apps.PollsConfig', #polls 앱 내에 있는 apps.py 파일 안의 PollsConfig 클래스를 불러옴 
    #이하 기본 제공 앱
    'django.contrib.admin', #관리용 사이트
    'django.contrib.auth', #인증 시스템
    'django.contrib.contenttypes', # 컨텐츠 타입을 위한 프레임워크
    'django.contrib.sessions', #세션 프레임워크
    'django.contrib.messages', #메세징 프레임워크
    'django.contrib.staticfiles', #정적 파일을 관리하는 프레임워크
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': { #sqlite일 경우 db를 자동 생성해주지만 아닐 경우 미리 db 생성을 해야함
        'ENGINE': 'django.db.backends.sqlite3', #db별 드라이버 설정 
        'NAME': BASE_DIR / 'db.sqlite3', #db명, db 파일을 저장할 절대경로+db명으로 설정함
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
