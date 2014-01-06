"""
Module that implements the actions for the CLI App when the label toplevel
command is used
"""

import arc.cli.actions.base
import arc.server


@arc.cli.actions.base.action
def status(app):
    """
    List host and jobs currently running on them

    :param app: the running application instance
    """
    to_human = {True: 'Yes',
                False: 'No'}
    stat = arc.server.get_status(app.connection)

    print("Concerns: %s" % to_human[stat["concerns"]])
    print("Scheduler Running: %s" % to_human[stat["scheduler_running"]])
    print("Scheduler Watcher Running: %s" % (
        to_human[stat["scheduler_watcher_running"]]))
    print("Install Server Running: %s" % (
        to_human[stat["install_server_running"]]))
    print("Log Disk Space Usage: %s%%" % stat["used_space_logs"])

    return stat["concerns"]

@arc.cli.actions.base.action
def list_install_profiles(app):
    """
    List the available installation profiles on the install server

    :param app: the running application instance
    """
    profiles = arc.server.get_profiles(app.connection)
    profiles = [x['name'] for x in profiles]
    for profile in profiles:
        if profile == 'N/A':
            break
        print profile
