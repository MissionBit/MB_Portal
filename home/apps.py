from django.apps import AppConfig
from django.db.models.signals import pre_migrate
from azure.storage.blob import PublicAccess


def ensure_azure_container(sender, **kwargs):
    """
    Ensure that the expected Azure Storage container exists when
    running with an emulated service.
    """
    from missionbit.azure_storage_backend import CustomAzureStorage

    if not CustomAzureStorage.is_emulated:
        return
    CustomAzureStorage().service.create_container(
        CustomAzureStorage.azure_container, public_access=PublicAccess.Blob
    )


class HomeConfig(AppConfig):
    name = "home"

    def ready(self):
        pre_migrate.connect(ensure_azure_container, sender=self)
