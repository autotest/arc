import arc.connection
import arc.host


c = arc.connection.get_default()
print("Server: %s" % c.hostname)
for h in arc.host.get_objs(c):
    print("Host: \t%s" % h.name)
    for i in h.FIELDS:
        print("\t%s: %s" % (i, getattr(h, i)))
    print("\tlabels: %s\n" % ", ".join(h.get_label_names()))
