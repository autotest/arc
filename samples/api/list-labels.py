import arc.connection
import arc.label


c = arc.connection.get_default()
print("Server: %s" % c.hostname)

for l in arc.label.get_objs(c):
    print("\n\t%s" % l.name)
    for i in l.FIELDS:
        print("\t%s: %s" % (i, getattr(l, i)))

