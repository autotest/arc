import sys

import arc.connection
import arc.host

c = arc.connection.get_default()

for service_name in arc.shared.rpc.PATHS:
    version = c.service_interface_versions.get(service_name, None)
    if version is not None:
        print("%s interface version: %s" % (service_name, version))
    else:
        print("%s interface version: Unknown" % service_name)
