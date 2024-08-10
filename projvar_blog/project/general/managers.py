from db.models import models


class CustomQuerySet(models.QuerySet):
	def get_or_none(self, *args, **kwargs):
		try:
			return self.get(*args, **kwargs)
		except self.model.DoesNotExist:
			return None


class CustomManager(models.Manager.from_queryset(CustomQuerySet)):
	pass

