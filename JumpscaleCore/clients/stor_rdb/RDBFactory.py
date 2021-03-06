import os
from Jumpscale import j

from .RDBClient import RDBClient

#
JSBASE = j.baseclasses.object


class RDBFactory(j.baseclasses.object):
    __jslocation__ = "j.clients.rdb"

    def _init(self):
        self._children = j.baseclasses.dict()

    def client_get(self, bcdbname=None, addr="localhost", port=6379, secret=None):
        """
        :param bcdbname: bcdbname name
        :param redisconfig_name: name of the redis config client see j.clients.redis_config
        :return:
        """
        assert bcdbname
        key = "%s_%s_%s" % (bcdbname, addr, port)
        if key not in self._children:
            self._children[key] = RDBClient(bcdbname=bcdbname, addr=addr, port=port, secret=secret)
        return self._children[key]

    def reset(self):
        def delete(db):
            itemstodel = ["queue:*", "rdb*", "myjobs*"]
            for item in itemstodel:
                for key in db.keys(item):
                    db.delete(key)

        delete(j.clients.redis.core)
        for item in self._children.values():
            item.flush()

    def test(self):
        """
        kosmos 'j.clients.rdb.test()'

        """
        cl = self.client_get("test")
        cl.flush()
        assert cl.count == 0
        assert len(cl.list()) == 0

        id = cl.set(b"INIT")
        assert id == 0
        assert cl.get(0) == b"INIT"

        nr = cl.count
        assert nr == 1
        # do test to see that we can compare
        id = cl.set(b"r")
        assert id == 1
        assert cl.get(id) == b"r"

        id2 = cl.set(b"b")
        assert id2 == 2

        assert cl.set(b"r", key=id) is None
        assert cl.set(b"rss", key=id) == 1  # changed the data, returns id 1

        nr = cl.count
        assert nr == 3  # nr of real data inside

        # test the list function
        assert cl.list() == [0, 1, 2]
        assert cl.list(2) == [2]
        assert cl.list(0) == [0, 1, 2]

        result = {}
        for id, data in cl.iterate():
            if id == 0:
                continue
            self._log_debug("%s:%s" % (id, data))
            result[id] = data

        assert {1: b"rss", 2: b"b"} == result

        assert cl.list(key_start=id2)[0] == id2

        assert cl.exists(id2)

        self._log_debug("write 10000 entries")

        def dumpdata(self):

            inputs = {}
            for i in range(1000):
                data = os.urandom(4096)
                key = cl.set(data)
                inputs[key] = data

            for k, expected in inputs.items():
                actual = cl.get(k)
                if expected != actual:
                    j.shell()
                assert expected == actual

        dumpdata(self)  # is in default bcdbname

        self._log_debug("count:%s" % cl.count)

        bcdbname = "newbcdbname"
        ns = self.client_get(bcdbname)
        ns.flush()
        assert ns.nsinfo["entries"] == 0

        # both should be same
        id = ns.set(b"a")
        assert ns.get(id) == b"a"
        assert ns.nsinfo["entries"] == 1

        nritems = 1000
        j.tools.timer.start("rdb")

        self._log_debug("perftest for 10.000 records, should get above 5k per sec, +10k expected")
        for i in range(nritems):
            id = cl.set(b"a")

        res = j.tools.timer.stop(nritems)

        assert res > 3000

        self._log_info("PERF TEST SEQ OK")

        cl.flush()
        ns.flush()

        return "OK"
