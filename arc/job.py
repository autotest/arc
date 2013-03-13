"""
Module with interface for fetching and manipulating jobs on an autotest server
"""


import functools

import arc.base
import arc.constants


__all__ = ['get_data',
           'get_ids',
           'get_names',
           'get_ids_names',
           'get_data_by_id',
           'get_data_by_name',
           'Job',
           'get_objs']


#
# Service on RPC server hosting these methods
#
SERVICE_NAME = arc.defaults.AFE_SERVICE_NAME


#
# Name of fields as defined on the server side database
#
ID_FIELD = 'id'
NAME_FIELD = 'name'


#
# Name of RPC methods as defined on the server side
#
GET_METHOD = 'get_jobs'
ADD_METHOD = 'create_job'


#
# Boiler plate code for remote methods that are generic enough to be reused
#
get_data = functools.partial(arc.base.get_data, SERVICE_NAME, GET_METHOD)
get_ids = functools.partial(arc.base.get_and_filter, get_data, ID_FIELD)
get_names = functools.partial(arc.base.get_and_filter, get_data, NAME_FIELD)
get_ids_names = functools.partial(arc.base.get_id_name_and_filter, get_data,
                                  ID_FIELD, NAME_FIELD)
get_data_by_id = functools.partial(arc.base.get_by, SERVICE_NAME, GET_METHOD,
                                   ID_FIELD)
get_data_by_name = functools.partial(arc.base.get_by, SERVICE_NAME, GET_METHOD,
                                     NAME_FIELD)


def add(connection, name, control_file, control_type, hosts):
    """
    Create and enqueue a job.

    :param connection:
    :param name: name of this job
    :param control_file: String contents of the control file.
    :param control_type: Type of control file, Client or Server.
    :param hosts: List of hosts to run job on.

    :returns: The created Job id number.
    """
    if (type(hosts) == str):
        hosts = hosts.split(' ')

    priority = arc.constants.JOB_PRIORITIES[1]

    return connection.run(SERVICE_NAME, ADD_METHOD, name, priority,
                          control_file, control_type, hosts)


def add_complete(connection,
                 name,
                 priority,
                 control_file,
                 control_type,
                 hosts=(),
                 profiles=(),
                 meta_hosts=(),
                 one_time_hosts=(),
                 atomic_group_name=None,
                 synch_count=None,
                 is_template=False,
                 timeout=None,
                 max_runtime_hrs=None,
                 run_verify=True,
                 email_list='',
                 dependencies=(),
                 reboot_before=None,
                 reboot_after=None,
                 parse_failed_repair=None,
                 hostless=False,
                 keyvals=None,
                 drone_set=None):
    """
    Create and enqueue a job.

    :param connection:
    :param name: name of this job
    :param priority: one of Low, Medium, High, Urgent
    :param control_file: String contents of the control file.
    :param control_type: Type of control file, Client or Server.
    :param synch_count: How many machines the job uses per autoserv execution.
                        synch_count == 1 means the job is asynchronous.
                        If an atomic group is given this value is treated as a
                        minimum.
    :param is_template: If true then create a template job.
    :param timeout: Hours after this call returns until the job times out.
    :param max_runtime_hrs: Hours from job starting time until job times out
    :param run_verify: Should the host be verified before running the test?
    :param email_list: String containing emails to mail when the job is done
    :param dependencies: List of label names on which this job depends
    :param reboot_before: Never, If dirty, or Always
    :param reboot_after: Never, If all tests passed, or Always
    :param parse_failed_repair: if true, results of failed repairs launched by
                                this job will be parsed as part of the job.
    :param hostless: if true, create a hostless job
    :param keyvals: dict of keyvals to associate with the job
    :param hosts: List of hosts to run job on.
    :param profiles: List of profiles to use, in sync with @hosts list
    :param meta_hosts: List where each entry is a label name, and for each
                       entry one host will be chosen from that label to run
                       the job on.
    :param one_time_hosts: List of hosts not in the database to run the job on.
    :param atomic_group_name: The name of an atomic group to schedule the job
                              on.
    :param drone_set: The name of the drone set to run this test on.

    :returns: The created Job id number.
    """
    if (type(hosts) == str):
        hosts = hosts.split(' ')

    return connection.run(SERVICE_NAME, ADD_METHOD,
                          name, priority, control_file, control_type,
                          hosts, profiles, meta_hosts, one_time_hosts,
                          atomic_group_name, synch_count, is_template,
                          timeout, max_runtime_hrs, run_verify,
                          email_list, dependencies, reboot_before,
                          reboot_after, parse_failed_repair, hostless,
                          keyvals, drone_set)


def delete(connection, numeric_id):
    """
    Deletes (unqueues, aborts) a Job queued on host machine(s)

    :param connection:
    :param numeric_id:
    """
    return connection.run(SERVICE_NAME,
                          "abort_host_queue_entries",
                          job=numeric_id)


class Job(arc.base.Model):
    """
    Interface for manipulating a job on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['control_file', 'control_type', 'created_on', 'dependencies',
              'drone_set', 'email_list', 'keyvals', 'max_runtime_hrs',
              'owner', 'parameterized_job', 'parse_failed_repair', 'priority',
              'reboot_after', 'reboot_before', 'run_verify', 'synch_count',
              'timeout']


    def __init__(self, connection, identification=None, name=None):
        super(Job, self).__init__(connection, identification, name)


    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)


    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)


    def delete(self):
        """
        Deletes (aka aborts) this job
        """
        return delete(self.connection, self.identification)


    abort = delete


    def __repr__(self):
        return "<Job ID: %s>" % self.id


get_objs = functools.partial(arc.base.get_objs, get_ids_names, Job)
