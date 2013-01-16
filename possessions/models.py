from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from middleware import get_current_user


class Possession(models.Model):
    owner = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    item_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey('content_type', 'item_id')

    class Meta:
        unique_together = ('content_type', 'item_id')


FORBBIDEN_MODELS = (
    Session,
    Possession,
)


@receiver(pre_save)
def pre_handler(sender, **kwargs):
    user = get_current_user()
    item = kwargs.get('instance')

    if sender in FORBBIDEN_MODELS:
        return None

    if not user or not user.is_active:
        return None

    if getattr(item, 'id', None):
        return None

    if hasattr(item, 'owner_id'):
        item.owner = user
    else:
        item._register_owner = True


@receiver(post_save)
def post_handler(sender, **kwargs):
    user = get_current_user()
    item = kwargs.get('instance')

    if getattr(item, '_register_owner', None) and user:
        try:
            p = Possession(item=item, owner=user)
            p.save()
        except:
            pass

