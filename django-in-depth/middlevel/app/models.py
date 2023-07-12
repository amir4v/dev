from datetime import timedelta
from typing import Iterable, Optional

from django.db import models
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()



class Car(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255, null=True, blank=True, default='Red')
    description = models.TextField(null=True, blank=True, default='car description')
    type = models.IntegerField(null=True, blank=True, default=1, choices=[
        (1, "Sedan"),
        (2, "Truck"),
        (4, "SUV"),
    ])



class File(models.Model):
    upload_to_path = 'files'
    upload_to = models.CharField(max_length=255, default='files')
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    path = models.FileField(upload_to=upload_to_path)
    cover = models.ImageField(upload_to=upload_to_path+'/cover')


from rest_framework_simplejwt.tokens import Token
class AccessToken(Token):
    token_type = "access"
    lifetime = None
    
    def __init__(self, lifetime, *args, **kwargs):
        self.lifetime = lifetime
        if self.lifetime is None:
            raise Exception("Access token must be specified with a lifetime!")
        super().__init__(*args, **kwargs)


class FileAccess(models.Model):
    def _100_years():
        return int(timedelta(days=100 * 356).total_seconds())
    def _5_minutes():
        return int(timedelta(minutes=5).total_seconds())
    lifetime_access = models.IntegerField(default=_100_years) # 100 Years
    lifetime_access_years = models.IntegerField(default=100)
    #
    temporary_access = models.IntegerField(default=_5_minutes) # 5 Minutes
    temporary_access_years = models.IntegerField(default=0)
    temporary_access_months = models.IntegerField(default=0)
    temporary_access_days = models.IntegerField(default=0)
    temporary_access_hours = models.IntegerField(default=0)
    temporary_access_minutes = models.IntegerField(default=5)
    #
    is_temporary = models.BooleanField(default=True)
    #
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    jwt_token = models.CharField(max_length=8001, default='', blank=True, null=True) # JWT Access Token
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    
    def save(self, *args, **kwargs):
        if self.is_temporary:
            lifetime = timedelta(seconds=self.temporary_access)
        else:
            lifetime = timedelta(seconds=self.lifetime_access)
        ##################
        if self.lifetime_access_years != 0 and self.lifetime_access_years != 100:
            self.lifetime_access = int(timedelta(days=self.lifetime_access_years * 356).total_seconds())
        
        
        
        
        temporary_access_time = 0
        
        if self.temporary_access_years != 0:
            temporary_access_time += int(timedelta(days=self.temporary_access_years * 356).total_seconds())
        
        if self.temporary_access_months != 0:
            temporary_access_time += int(timedelta(days=self.temporary_access_months * 30).total_seconds())
        
        if self.temporary_access_days != 0:
            temporary_access_time += int(timedelta(days=self.temporary_access_days).total_seconds())
        
        if self.temporary_access_hours != 0:
            temporary_access_time += int(timedelta(hours=self.temporary_access_hours).total_seconds())
        
        if self.temporary_access_minutes != 0:
            temporary_access_time += int(timedelta(minutes=self.temporary_access_minutes).total_seconds())
        
        if temporary_access_time != 0:
            self.temporary_access = temporary_access_time
        ########################3
        
        
        if self.is_temporary and temporary_access_time != 0:
            lifetime = timedelta(seconds=temporary_access_time)
        elif self.is_temporary and temporary_access_time == 0:
            lifetime = timedelta(seconds=self.temporary_access)
        elif not self.is_temporary:
            lifetime = timedelta(seconds=self.lifetime_access)
        
        access_token = AccessToken(lifetime=lifetime)
        access_token.payload['file_path'] = str(self.file.path)
        
        # for_user and user_id is for checking the comming user_id from jwt is the same user_id of cureent user
        if self.user:
            access_token.payload['user_id'] = self.user.id
        else:
            access_token.payload['user_id'] = None
        
        self.jwt_token = str(access_token)
        
        return super().save(*args, **kwargs)
    
    """
    class AccessToken(Token):
        token_type = "access"
        lifetime = api_settings.ACCESS_TOKEN_LIFETIME
    from rest_framework_simplejwt.tokens import AccessToken
    access_token = AccessToken()
    access_token.payload['user_id'] = user.id or None
    access_token.payload['email'] = user.email
    return str(access_token)
    import jwt
    from rest_framework_simplejwt.state import api_settings
    _token = jwt.decode(
                jwt=token, key=settings.SECRET_KEY,
                algorithms=[api_settings.ALGORITHM]
            )
            email = _token.get("email")
    access_token = AccessToken()
    access_token.payload['user_id'] = user.id or None
    access_token.payload['email'] = user.email
    return str(access_token)
    try:
        _token = jwt.decode(
            jwt=token, key=settings.SECRET_KEY,
            algorithms=[api_settings.ALGORITHM]
        )
        email = _token.get("email")
    except ExpiredSignatureError:
        return Response(
            {"detail": "Token has been expired!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except InvalidSignatureError:
        return Response(
            {"detail": "Token is invalid!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception:
        return Response(
            {"detail": "Token is not valid!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    #
    user_id
    #
    is user
    is active
    is verified
    is staff
    is superuser
    has permission
    group access
    just an access token
    temporary access token
    """
#


@deconstructible
class FileSizeValidator:
    message = 'file size!!! error'
    code = 'file_size'

    def __init__(self, size, message=None, code=None):
        self.size = size

    def __call__(self, file):
        if file.size > self.size:
            raise ValidationError('size ig >')


class PostPicture(models.Model):
    picture = models.ImageField(upload_to='images/pictures', validators=[
        validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif']),
        validators.ProhibitNullCharactersValidator(),
        FileSizeValidator(1 * 1024 * 1024)
    ])
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, default=None)
    content = models.TextField(blank=True, null=True, default=None)
    banner = models.CharField(max_length=1000, blank=True, null=True, default=None)
    txt_file = models.FilePathField(path='./', recursive=True, blank=True, null=True, default=None) # match='*.py'
    some_file = models.FileField(upload_to='files/anything', blank=True, null=True, default=None)


class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_picture = models.ForeignKey(PostPicture, on_delete=models.CASCADE)
