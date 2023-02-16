from django.db import models


class Memory(models.Model):
    ip = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
    # HasDone_HitNumber = models.IntegerField(default=-1)
    # FromThisEpoch = models.IntegerField(default=-1)
    throttle = models.CharField(max_length=200, null=True, default=None) # n_t_t # HasDoneHitNumber_FromThisEpoch


# on an action
class Limit(models.Model):
    # name
    limit = models.CharField(max_length=50, null=True, default=None) # hit/per
    pass


class LimitMemory(models.Model):
    # in ip/user/group N ta hit dashte dar in (limit)
    # ip
    # hit
    # limit
    pass


class Throttle(models.Model):
    def __init__(self, name, target):
        self.limit = Limit.objects.get(name=name)
        pass
    
    def invalid(self):
        lm = LimitMemory.get(target=target, ip=ip, limit=limit)
        if lm.hit > lm.limit.hit:
            True # means Yes it's invalid and over
            # return HTTPBadRequest(400, 'limit has reach error')
        pass
    
    # limit
    # target: ip
    pass


# class View(models.Model):
#     name = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
#     limit = models.CharField(max_length=50, null=True, default=None) # hit/per
# #
# #
# class ViewMemory(models.Model):
#     ip = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
#     throttle = models.CharField(max_length=200, null=True, default=None) # n_t_t
#     # memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    
#     view = models.ForeignKey(View, null=True, default=None, on_delete=models.CASCADE, related_name='view_memories')
