import arc.connection
import arc.job


c = arc.connection.get_default()

# 1st approach, object like interface
print("Jobs List")
for job in arc.job.get_objs(c):
    print("%s\t%s" % (job.identification, job.name))

# 2nd approach, raw data manipulation
print("Jobs List")
for job in arc.job.get_data(c):
    print("%s\t%s" % (job["id"], job["name"]))
