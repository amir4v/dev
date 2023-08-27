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
		# if in seen and in result that mean is related
		# if in seen not in relates that mean is not related
		if cls in seen:
			if cls in result:
				return True
			return False
		else:
			# save to seen list for preventing the infinity incursion loop error
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
				# add current model/cls which is the base model and add all models that are related to this model
				result.append(cls)
				for field_ in _meta_get_fields:
					type__ = field_.__class__
					if type__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
						result.append(field_.related_model)
			return True
		
		for field in _meta_get_fields:
			type_ = field.__class__
			
			if type_ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
				if field.related_model == the_model or field.related_model in result:
					# add current model/cls add all models that are related to this model
					result.append(cls)
					result.append(field.related_model)
					for field_ in _meta_get_fields:
						type__ = field_.__class__
						if type__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
							result.append(field_.related_model)
					return True
				else:
					# Even having one relation is enough to be related
					flag = inner(field.related_model) or flag
					if flag:
						# add current model/cls add all models that are related to this model
						result.append(cls)
						result.append(field.related_model)
						for field_ in _meta_get_fields:
							type__ = field_.__class__
							if type__ in [models.OneToOneField, models.ForeignKey, models.ManyToManyField]:
								result.append(field_.related_model)
		
		if flag:
			# add current model/cls add all models that are related to this model
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
	# add None for pushing the middle Model forward to get involved in the next loop
	given_models.append(None)
	# find relations in reverse state of given_models because covering all states of checking if a model's relation is in the result or not
	for model in given_models[::-1]:
		seen = [None]
		inner(model)
	
	while None in result:
		result.remove(None)
	return set(result)
