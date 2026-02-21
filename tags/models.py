import re
from functools import reduce
from operator import and_, or_

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

_TERMS = re.compile(r'"([^"]+)"|(\S+)').findall
_NORM_SPACE = re.compile(r'\s{2,}').sub


def _normalize_query(query_string):
    return [
        _NORM_SPACE(' ', (t[0] or t[1]).strip())
        for t in _TERMS(query_string)
    ]


def _search_q(search_fields, terms):
    if not terms:
        return None
    q_per_term = (
        reduce(or_, (Q(**{f"{f}__icontains": term}) for f in search_fields))
        for term in terms
    )
    return reduce(and_, q_per_term)


class TagQuerySet(models.QuerySet):
    def find(self, query):
        q = _search_q(['text'], _normalize_query(query or ''))
        return self.filter(q) if q is not None else self.none()


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def find(self, query):
        return self.get_queryset().find(query)


class TagGroupQuerySet(models.QuerySet):
    def find(self, query):
        return self.filter(tags__in=Tag.objects.find(query))


class TagGroupManager(models.Manager):
    def get_queryset(self):
        return TagGroupQuerySet(self.model, using=self._db)

    def find(self, query):
        return self.get_queryset().find(query)


class TagGroup(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)

    objects = TagGroupManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = _('Tag group')
        verbose_name_plural = _('Tag groups')


class Tag(models.Model):
    group = models.ForeignKey(
        TagGroup,
        verbose_name=_('Group'),
        on_delete=models.SET_NULL,
        related_name='tags',
        null=True,
        blank=True,
    )
    text = models.CharField(_('Text'), max_length=255, db_index=True)

    objects = TagManager()

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ('group', 'text', )
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
