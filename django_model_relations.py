from django.db import models


def relations(the_model, given_models):
	"""
	This function gives you all models including itself that are somehow
	related to this model either OneToOne or ForeignKey or ManyToMany.
	It covers all kind of relations like: 1-1, 1-n, n-n.
	"""
	
	result = []
	
	# The Begin of the inner function
	def inner(cls):
		if cls is None:
			return False
		
		# Return True because you are already known as a related
		if cls in seen:
			if cls in result:
				return True
			return False
		else:
			seen.append(cls)
		
		flag = False
		try:
			_meta_get_fields = cls._meta.get_fields()
		except:
			# It's not a conventional Django Model
			return False
		
		# If it's the base Model itself, return True
		if cls == the_model:
			if cls not in result:
				result.append(cls)
				for field_ in _meta_get_fields:
					type__ = field_.__class__
					if type__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
						result.append(field_.related_model)
			return True
		
		for field in _meta_get_fields:
			type_ = field.__class__
			
			if type_ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
				if field.related_model == the_model:
					result.append(cls)
					for field_ in _meta_get_fields:
						type__ = field_.__class__
						if type__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
							result.append(field_.related_model)
					return True
				else:
					# Even having one relation is enough to be related
					flag = inner(field.related_model) or flag
					if flag:
						result.append(cls)
						result.append(field.related_model)
						for field_ in _meta_get_fields:
							type__ = field_.__class__
							if type__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
								result.append(field_.related_model)
		
		if flag:
			result.append(cls)
			for field_ in _meta_get_fields:
				type__ = field_.__class__
				if type__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
					result.append(field_.related_model)
		return flag
	# The End of the inner function
	
	for model in given_models:
		seen = [None]
		inner(model)
	
	while None in result:
		result.remove(None)
	return set(result)
