import sys

import arc.connection
import arc.host


host_id = sys.argv[1]

c = arc.connection.get_default()
h = arc.host.get_data_by_id(c, host_id)
if h is not None:
    print("Found host with id %s, name is %s" % (host_id,
                                                 h['hostname']))
