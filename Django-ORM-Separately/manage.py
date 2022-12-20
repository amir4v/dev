def init_django():
    import django
    from django.conf import settings

    # if settings.configured:
    #     return

    settings.configure(
        INSTALLED_APPS=[
            'app',
        ],
        
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            },
            
            # 'default': {
            #     'ENGINE': 'django.db.backends.DB',
            #     'NAME': 'DB-Name',
            #     'USER': 'Username',
            #     'PASSWORD': 'Password',
            #     'HOST': 'Host-Address',
            #     'PORT': '-PORT-',
            # }
        }
    )
    
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
