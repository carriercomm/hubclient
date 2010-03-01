"""
Environment variables:

    HUB_SERVERCONF      default: /etc/hubclient/server.conf
"""

import os

class ConfFile(dict):
    """Configuration file class (targeted at simple shell type configs)

    Usage:

        class foo(ConfFile):
            CONF_FILE = /path/to/conf

        print foo.key1      # display KEY1 value from /path/to/conf
        foo.key2 = value    # set KEY2 value
        foo.write()         # write new config to /path/to/conf

    """
    CONF_FILE = None

    def __init__(self):
        self.read()

    def read(self):
        if not self.CONF_FILE or not os.path.exists(self.CONF_FILE):
            return 

        for line in file(self.CONF_FILE).readlines():
            line = line.rstrip()

            if not line or line.startswith("#"):
                continue

            key, val = line.split("=")
            self[key.strip().lower()] = val.strip()

    def write(self):
        fh = file(self.CONF_FILE, "w")
        items = self.items()
        items.sort()
        for key, val in items:
            print >> fh, "%s=%s" % (key.upper(), val)

        fh.close()

    def items(self):
        items = []
        for key in self:
            items.append((key, self[key]))

        return items

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, e:
            raise AttributeError(e)

    def __setattr__(self, key, val):
        self[key] = val

class HubServerConf(ConfFile):
    CONF_FILE = os.getenv('HUB_SERVERCONF', '/etc/hubclient/server.conf')

