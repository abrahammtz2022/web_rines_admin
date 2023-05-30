import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# psycopg2

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bdrines',
        'USER': 'postgres',
        'PASSWORD': 'rfs980102cg8',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

#conectar nube
NUBEWEB = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'wAI7OA96tpck5k16OSzZ',
        'HOST': 'containers-us-west-95.railway.app',
        'PORT': '7572'
    }
}

# mysqlclient

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pos',
        'USER': 'root',
        'PASSWORD': 'admin12345678',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
