import arc.connection
import arc.linuxdistro

c = arc.connection.get_default()
print("Server: %s" % c.hostname)
for h in arc.linuxdistro.get_objs(c):
    print("LinuxDistro: \t%s" % h.name)
    for i in h.FIELDS:
        print("\t%s: %s" % (i, getattr(h, i)))

