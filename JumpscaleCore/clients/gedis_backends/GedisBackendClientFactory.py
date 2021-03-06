from Jumpscale import j
from .GunClient import GunClient

JSConfigBase = j.baseclasses.factory

ALLOWED_TYPES = {"gun": GunClient}  # available clients, add to this if a new client is added


class GedisBackendClientFactory(JSConfigBase):
    __jslocation__ = "j.clients.gedis_backend"

    _CHILDCLASS = GunClient

    def get(self, instance="main", data=None, create=True, die=True, interactive=True, type="gun"):
        if data is None:
            data = {}
        if not create and instance not in self.list():
            if die:
                raise j.exceptions.Base("could not find instance:%s" % (instance))
            else:
                return None
        if type not in ALLOWED_TYPES:
            raise j.exceptions.Base("Specified type not allowed")
        return ALLOWED_TYPES[type](instance=instance, data=data, interactive=interactive, parent=self)
