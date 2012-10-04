import arc.connection
import arc.label


c = arc.connection.get_default()

l = arc.label.Label(c)
l.identification = 1
print(l.get_data())


l2 = arc.label.Label(c)
l2.name = 'intel64'
print(l2.get_data())
