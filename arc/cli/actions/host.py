"""
Module that implements the actions for the CLI App when the host toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.host


OBJ_NAME = "host"


list_brief = functools.partial(arc.cli.actions.base.list_brief,
                               arc.host.get_objs)


add = functools.partial(arc.cli.actions.base.add_with_name,
                        OBJ_NAME, arc.host.add)


delete = functools.partial(arc.cli.actions.base.delete,
                           OBJ_NAME, arc.host.Host, arc.host.delete)


def list_jobs(app):
    """
    List host and jobs currently running on them

    :param app: the running application instance
    """
    def get_job_id_name(queue, host_id):
        for j in queue:
            if j['host']['id'] == host_id:
                return (j['id'], j['job']['name'])
        return ('', '')

    line_fmt = "%-6s%-34s%-8s%-80s"
    header = line_fmt % ("ID", "NAME", "JOB ID", "JOB NAME")
    header_printed = False
    queue = app.connection.run('get_host_queue_entries', active=True)
    hosts = arc.host.get_objs(app.connection)
    for h in hosts:
        if not header_printed:
            print(header)
            header_printed = True

        (job_id, job_name) = get_job_id_name(queue, h.identification)

        print(line_fmt % (h.identification,
                          h.name,
                          job_id,
                          job_name))
