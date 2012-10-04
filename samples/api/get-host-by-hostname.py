import sys

import arc.connection
import arc.host


host_name = sys.argv[1]

c = arc.connection.get_default()
h = arc.host.get_data_by_name(c, host_name)
if h is not None:
    print("Found host with name %s, id is %s" % (host_name,
                                                 h['id']))
