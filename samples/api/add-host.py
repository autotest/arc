import sys

import arc.connection
import arc.host


name = sys.argv[1]
arc.host.add(arc.connection.get_default(), name)
