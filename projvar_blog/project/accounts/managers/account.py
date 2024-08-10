from django.apps import apps
from django.contrib.auth.hashers import make_password

from general.managers import CustomManager


class UserManager(CustomManager):
	def _create_user(self, username, password, **extra_fields):
		"""
		Create and save a user with the given username, and password.
		"""
		if not all([username, password]):
			raise ValueError("The given username must be set")
		GlobalUserModel = apps.get_model(
			self.model._meta.app_label, self.model._meta.object_name
		)
		username = GlobalUserModel.normalize_username(username)
		user = self.model(username=username, **extra_fields)
		user.password = make_password(password)
		user.save(using=self._db)
		return user
	
	def create(self, username, password, **extra_fields):
		return self._create_user(username, password, **extra_fields)
	
	def create_user(self, username, password, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(username, password, **extra_fields)
	
	def create_superuser(self, username, password, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)
		
		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")
		
		return self._create_user(username, password, **extra_fields)
