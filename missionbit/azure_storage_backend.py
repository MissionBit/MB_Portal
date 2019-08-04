from django.utils.deconstruct import deconstructible
from azure.storage.blob.blockblobservice import BlockBlobService
from storages.backends.azure_storage import AzureStorage
from storages.utils import setting

@deconstructible
class CustomAzureStorage(AzureStorage):
    # This is a workaround for AzureStorage to support custom domains
    custom_domain = setting('AZURE_CUSTOM_DOMAIN', None)

    @property
    def service(self):
        if self._service is None:
            self._service = BlockBlobService(
                self.account_name,
                self.account_key,
                is_emulated=self.is_emulated,
                custom_domain=self.custom_domain)
        return self._service

    def url(self, name, expire=None):
        url = super().url(name, expire=expire)
        if self.is_emulated and url.startswith('https://azurite:'):
            url = url.replace('https://azurite:', 'http://localhost:')
        return url
