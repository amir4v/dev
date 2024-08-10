from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from general.utils.random import get_random_username
from ..managers.account import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	"""
	Customized User-Model
	key fields are username and password; which they are also
	the basic information for authentication plus an arbitrary field called
	email which optional at this point but it'll be the same important as
	the current username.
	Field name is optional.
	"""
	
	username = models.CharField(
		_("username"),
		max_length=32,
		unique=True,
		db_index=True,
		default=get_random_username,
		help_text=_(
			"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
		),
		validators=[],
		error_messages={
			"unique": _("A user with that username already exists."),
		},
	)
	name = models.CharField(_("name"), max_length=150, blank=False, null=True, default=None)
	email = models.EmailField(_("email address"), blank=False, null=True, default=None)
	is_superuser = models.BooleanField(
		_("superuser status"),
		default=False,
		help_text=_("Designates whether the user is a superuser or not."),
	)
	is_staff = models.BooleanField(
		_("staff status"),
		default=False,
		help_text=_("Designates whether the user can log into this admin site."),
	)
	is_active = models.BooleanField(
		_("active"),
		default=True,
		help_text=_(
			"Designates whether this user should be treated as active. "
			"Unselect this instead of deleting accounts."
		),
	)
	
	objects = UserManager()
	
	EMAIL_FIELD = "email"
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["username", "password"]
