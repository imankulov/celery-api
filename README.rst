Celery API discovery module
---------------------------

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

.. note::
    If you can't launch the task and get a NotRegistered exception instead,
    it's most likely you have the ``CELERY_ALWAYS_EAGER`` config option set to
    ``True``.
