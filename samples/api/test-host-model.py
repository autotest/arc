import sys

import arc.connection
import arc.host


h = arc.host.Host(arc.connection.get_default(), identification=sys.argv[1])
exists_remotely = h.load_data()
print("Host exists remotely: %s" % exists_remotely)
if exists_remotely:
    print("Hostname: %s" % h.name)
    for i in h.FIELDS:
        print("%s: %s" % (i, getattr(h, i)))
