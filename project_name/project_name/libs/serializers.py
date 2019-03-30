"""Custom Django DRF serializers"""
from rest_framework import serializers


class AuditedModelSerializerString(serializers.ModelSerializer):
    """Serialize audited model, related users as string"""
    create_by = serializers.StringRelatedField(many=True)
    update_by = serializers.StringRelatedField(many=True)
    common_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']


class AuditedModelSerializerIds(serializers.ModelSerializer):
    """ Field create_by is a Foreign Key. So with this serialization we will
        obtain a list of ids.
    """
    create_by = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    update_by = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

class AuditedModelSerializer(serializers.ModelSerializer):
    """Add of field common_fields to use in our serializers"""
    common_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
