import arc.connection
import arc.host


c = arc.connection.get_default()
for i in arc.host.get_ids(c):
    arc.host.delete(c, i)
