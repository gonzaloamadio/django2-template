"""
    Model that add generic behaviour. Inherit from this in apps models.
"""
from django.conf import settings
from django.db import models

from . import global_request
from .shortuuid import encode
import uuid

class UUIDPrimaryKey(models.Model):
    """
    An abstract base class model that provides
    primary key id as uuid.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def friendly_id(self):
        return encode(self.id)

    class Meta:
        abstract = True

class ValidateOnSave(models.Model):
    """
        Inherit from this class to explicit call full_clean on fields.
        What we achieve with this, is do the same as if we were creating an
        instance from a form, but when we do it programatically, calling to
        save() or create()

        NOTE: Clean is not called when we perform ORM operations like
        update, select_for_update, bulk_create etc.
        They will all completely bypass this.
    """

    def save(self, force_insert=False, force_update=False, **kwargs):
        # p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
        # Its the same as:
        # p = Person(first_name="Bruce", last_name="Springsteen")
        # p.save(force_insert=True)
        # So we do not want this if, because we want to call full_clean on
        #   creation to

        #if not (force_insert or force_update):
        #    self.full_clean()

        self.full_clean()
        super(ValidateOnSave, self).save(force_insert, force_update,
                                              **kwargs)

    class Meta:
        abstract = True

class AuditedModel(models.Model):
    """
    TODO: CHECK IF THIS IS TRUE

    CAVEAT 1:
    If using a custom user model, add the following line to the top:
    from api.models.user_profile import User  # noqa: F401
    It's needed for get_model in settings.
    CAVEAT 2:
    All api calls that add or edit a line to your database should be Authenticated.
    If you're not doing that then you are ASKING for trouble.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_create',
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_update',
        null=True,
        blank=True,
    )

    class Meta: # pylint: disable=missing-docstring,too-few-public-methods
        abstract = True
        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_at', '-updated_at']

    def save(self, *args, **kwargs): # pylint: disable=arguments-differ
        """
        Store create_user if it's not assigned yet (first time the object is
        saved() and overwrite the update_user
        """
        current_user = global_request.get_current_user()
        if current_user:
            if not self.created_by:
                self.created_by = current_user
            self.updated_by = current_user

        return super(AuditedModel, self).save(*args, **kwargs)


class PersistentModelQuerySet(models.QuerySet):
    """Model implementing QuerySet for PersistentModel: allows soft-deletion"""

    def delete(self):
        self.update(deleted=True)


class PersistentModelManager(models.Manager):
    """Model implementing default manager for PersistenModel: filters 'deleted' elements"""

    def deleted(self, *args, **kwargs):
        return super().all(*args, **kwargs).filter(deleted=True)

    def not_deleted(self, *args, **kwargs):
        return super().all(*args, **kwargs).filter(deleted=False)

    def filter(self, *args, **kwargs):
        """Filter active instances"""
        active_only = kwargs.pop('active_only', True)
        deleted = kwargs.pop('deleted', False)
        qset = super().filter(*args, **kwargs)
        if deleted:
            return qset.filter(deleted=True)
        if active_only:
            return qset.filter(deleted=False)
        return qset

    def all(self, *args, **kwargs):
        """return all instanes"""
        active_only = kwargs.pop('active_only', True)
        qset = super().all(*args, **kwargs)
        if active_only:
            return qset.filter(deleted=False)
        return qset

    def get_queryset(self, **kwargs): # pylint: disable=unused-argument
        """Get queryset method"""
        return PersistentModelQuerySet(self.model, using=self._db)


class PersistentModel(models.Model):
    """Abstract class allowing soft-deletion"""

    deleted = models.BooleanField(default=False)
    objects = PersistentModelManager()

    class Meta: # pylint: disable=missing-docstring,too-few-public-methods
        abstract = True

    def delete(self): # pylint: disable=arguments-differ
        """Mark an instance as deleted, soft delete"""
        self.deleted = True
        self.save()


class CodeModel(models.Model):
    """
        Agregamos esta variable solo para mostrar algun codigo, que lo formamos
        con el id del objeto.
        Entonces por ejemplo si tenemos una lista de objetos, y necesitamos nombrarlos
        podemos usar esto.
        Por ejemplo, tenemos una clase class Alumno que extiende esta clase y sobre
        escribimos esta variable como _CODE_FORMAT = 'AL-{id:06d}', y al imprimir
        una lista de alumnos mostramos el code, veremos algo como
        AL-000001, AL-000002,  . . .
    """

    _CODE_FORMAT = 'code-{id:06d}'

    class Meta: # pylint: disable=missing-docstring,too-few-public-methods
        abstract = True

    @property
    def code(self):
        """Provided the pk exists, return CODE for instance"""
        return self._CODE_FORMAT.format(id=self.pk)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
