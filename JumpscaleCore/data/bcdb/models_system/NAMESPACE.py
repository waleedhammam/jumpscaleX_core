from Jumpscale import j


class NAMESPACE(j.data.bcdb._BCDBModelClass):
    def _schema_get(self):
        return j.data.schema.get_from_url("jumpscale.bcdb.meta.namespace.2")

    @property
    def acl(self):
        raise j.exceptions.Base("cannot modify acl object in acl object")
