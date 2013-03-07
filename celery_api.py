# -*- coding: utf-8 -*-
"""
Celery API discovery module.
"""
from celery import Celery


def make_api(*args, **kwargs):
    """
    Little shortcut for api discovery
    """
    celery = Celery(*args, **kwargs)
    return CeleryApi(celery)


class CeleryApi(object):
    """
    Celery API discovery class.

    Given the celery instance, it inspects all available celery workers to get
    the information about the queues they serve and tasks they know about.

    Then it creates a chain of attributes allowing to execute any task as
    ``queue_name.full_task_name.delay``.

    With help of this class you can turn your Celery installation to a set of
    independent modules, each of which "exposes" its own "Celery API".

    To make it more clear, the analogy with a random HTTP-based API available
    at http://example.com/users/get?email=john@example.com can be like:

    - Celery object (including broker URL, result backend settings, etc) is the
      analogue of the protocol (http://)
    - Queue name is the analogue of the hostname (example.com)
    - Task name is the analogue of the URL path (/users/get)
    - Task parameters the the analogue the querystring (?email=john@example.com)

    Usage example.

    If we have a Celery installation with two queues:
    "download" (knows how to execute "downloader.download_url" task) and
    "parse" (knows how to execute "parser.parse_html"), we can instantiate
    API and work with it the following way:

    .. code-block:: python

        >>> api = celery_api.CeleryApi(celery)
        >>> html_page = api.download.downloader.download_html.delay('http://example.com').get()
        >>> html_tree = api.parse.parser.parse_html.delay(html_page).get()

    .. note::
        Ensure that workers are up and available from clients for inspection.
        You may re-discover your installation after object creation by executing
        ``api._discover()``.
    """

    def __init__(self, celery):
        self._celery = celery
        self._inspect = self._celery.control.inspect()
        self._discover()

    def _discover(self):
        """
        Discover and expose the API by creating a chain of object attributes
        """
        for queue_name, task_list in self._get_tasks().items():
            if not hasattr(self, queue_name):
                setattr(self, queue_name, TaskProxy())
            queue = getattr(self, queue_name)

            for task_name in task_list:
                chunks = task_name.split('.')  # ['foo', 'bar', 'do_smth']
                current = queue
                for chunk in chunks[:-1]:
                    if not hasattr(current, chunk):
                        setattr(current, chunk, TaskProxy())
                    current = getattr(current, chunk)
                task = self._celery.Task()
                task.name = task_name
                setattr(current, chunks[-1], task)

    def _get_tasks(self):
        """
        Helper function: get the dict: queue_name -> [task name, ...]
        """
        queues = {}
        # get the list of registered tasks: worker -> [task1, task2, ...]
        registered = self._inspect.registered()

        active_queues = self._inspect.active_queues() or {}
        for worker_name, queue_info_list in active_queues.items():
            for queue_info in queue_info_list:
                queue_name = queue_info['name']
                queues.setdefault(queue_name, set())
                worker_tasks = registered.get(worker_name, [])
                queues[queue_name].update(worker_tasks)

        return queues


class TaskProxy(object):
    pass

