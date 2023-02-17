from time import time
import datetime
import calendar
from django.db import models
from django.core.exceptions import BadRequest
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from .middleware import LIMIT_DURATION


User = get_user_model()


class Memory(models.Model):
    """Remembers who requested and how many times requested and from when"""
    
    # ip = models.CharField(max_length=100, unique=True, db_index=True, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # group
    
    hit = models.IntegerField(default=0) # HasDone_HitNumber
    
    """Will Initiate on first hit and when it's over the limitation"""
    From = models.IntegerField(default=0) # FromThisEpoch
    
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} - ({self.condition}) - {self.hit}'


class Limit(models.Model):
    """On an action/view"""
    
    name = models.CharField(max_length=100, unique=True, db_index=True, blank=False, null=False)
    
    def get_conditions_durations(self):
        conditions = self.condition_set.all()
        conditions = [(condition, condition.duration) for condition in conditions]
        conditions = sorted(conditions, key=lambda c: c[1], reverse=True)
        return conditions
    
    def __str__(self):
        return self.name


class Condition(models.Model):
    condition = models.CharField(max_length=100, blank=False, null=False) # hit/duration -> 'Hit-Number/Per(s/min/h/d/w/month/y)'
    limit = models.ForeignKey(Limit, on_delete=models.CASCADE)
    
    @property
    def duration(self):
        hit, n_duration = self.condition.split('/')
        hit = int(hit)
        
        n, duration = n_duration.split(':')
        n = int(n)
        
        duration = n * LIMIT_DURATION.get(duration)
        
        return duration
    
    def __str__(self):
        return f'{self.limit} - {self.condition}'


def action_throttle(user: User, limit, raise_exception=True):
    """Limit Throttle function for an action"""
    now = int(time())
    
    limit = Limit.objects.get(name=limit)
    # conditions = limit.condition_set.all()
    conditions = limit.get_conditions_durations()
        
    ################################################################################################
    for condition, durations in conditions: # Vaghti condition bozorgaro naghz kardi dige soraghe kochike nemiri
        # First time
        memory, created = Memory.objects.get_or_create(user=user, condition=condition)
        if created:
                memory.hit = 1
                memory.From = now
                memory.save()
                return True
        user_hit_number = memory.hit
        user_hit_from = memory.From
        
        condition = condition.condition
        
        hit, n_duration = condition.split('/')
        hit = int(hit)
        
        n, duration = n_duration.split(':')
        n = int(n)
        
        duration = n * LIMIT_DURATION.get(duration)
        until = user_hit_from + duration
        
        if (now < until) and (user_hit_number >= hit):
            if raise_exception:
                raise BadRequest("You've reached the limit.")
            else:
                return False
        elif now >= until:
            memory.hit = 1
            memory.From = now
            memory.save()
        else:
            memory.hit += 1
            memory.save()
    ################################################################################################
    return True
