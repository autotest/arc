import sys

import arg.host
import arc.connection


hostname = sys.argv[1]
key = sys.argv[2]
val = sys.argv[3]
d = {key: val}

arc.host.modify(arc.connection.get_default(),
                hostname, **d)
