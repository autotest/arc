import arc.connection
import arc.tko.job


c = arc.connection.get_default()

print(arc.tko.job.get_data(c))
