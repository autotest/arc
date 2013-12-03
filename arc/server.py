"""
Module with interface for interacting with server status
"""

import arc.shared.frontend


__all__ = ['get_status']


def get_status(connection):
    '''
    Returns the general status of the Autotest server

    The returned information includes the status of essential services, such
    as the Autotest scheduller processes, the disk usage on the log filesystem
    (the one that is more likely to grow and cause issues). If an external
    install server is configured, it's also checked.

    Finally, one piece of information summarizes all the previously described
    information and determines wheter there's something to be concerned about
    the current status of the Autotest server.

    :param connection: an active connection to the Autotest server
    :type connection: `class:arc.connection.Connection`
    :returns: a dictionary containing the following keys: `concerns`,
              `scheduler_running`, `scheduler_watcher_running`,
              `install_server_running`, `used_space_logs`
    :rtype: dict
    '''
    return connection.run(arc.shared.frontend.AFE_SERVICE_NAME,
                          'get_server_status')
