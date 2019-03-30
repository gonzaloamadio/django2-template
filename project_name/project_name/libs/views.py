"""File with combination of classes to inherit in our apps"""
from rest_framework import mixins, viewsets

from .pagination import CustomPagination


class APIPaginatedViewSet(viewsets.GenericViewSet):
    pagination_class = CustomPagination


class APIViewSet(
        APIPaginatedViewSet,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
):
    """All operations"""
    def perform_create(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(updated_by=self.request.user)


class APIReadOnlyViewSet(
        APIPaginatedViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    """List and retrieve operations"""
    pass


class APIListRetrieveUpdateViewSet(
        APIPaginatedViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
):
    """List, retrieve and update operations"""
    def perform_update(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(updated_by=self.request.user)
