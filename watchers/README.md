## `data_freshness`

A watcher that checks for freshness of data in a given SQL table, with customizable query and threshold.

Checks run every minute, alerts sent every 5 minutes. Each table can have different alert targets.

## `ssh_check`

A watcher that runs commands over SSH and alerts if any fail or return a blank response.

The commands are provided in an array to be passed to `subprocess.check_output()`.

Checks run every minute, alerts sent every 5 minutes. Each check can have different alert targets.

## `url_check`

A watcher that verifies a given URLs returns HTTP 200 using a GET request and a common browser User-Agent.

Optional per-URL config parameters:
* `user_agent`: provide a custom User-Agent string
* `response`: run `re.search()` on the response with the given pattern
* `latency`: maximum latency in milliseconds

Checks run every minute, alerts sent every 5 minutes. Each check can have different alert targets.
