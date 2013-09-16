import arc.server
import arc.connection

c = arc.connection.get_default()
status = arc.server.get_status(c)

print("Concerns: %s" % status["concerns"])
print("Scheduler Running: %s" % status["scheduler_running"])
print("Scheduler Watcher Running: %s" % status["scheduler_watcher_running"])
print("Install Server Running: %s" % status["install_server_running"])
print("Log Disk Space Usage: %s%%" % status["used_space_logs"])
