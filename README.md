# Watcher

A simple framework for easy definition and deployment of custom monitoring and alerting.

A watcher corresponds to a `watchers/[watcher_name].py` file, which defines a `Watcher` class with a `run()` method.

Each watcher is run separately using the `./run.py` command, its `run()` method is expected to run continuously.

## Install

1. Clone this repo
2. `./build-venv.sh`

## Configure

Copy `config.yaml.example` to `config.yaml` and adjust as appropriate.

## Run

To run a watcher from your console:
```bash
source venv/bin/activate
./run.py --debug [watcher_name]
```

Sample definition of a `watcher-[watcher-name].service`:
```ini
[Unit]
Description=Watcher
After=network.target

[Service]
WorkingDirectory=/path/to/watcher
ExecStart=/bin/bash -c "source /path/to/watcher/venv/bin/activate; exec /path/to/watcher/run.py [watcher_name]"
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Contribute

In order to create a new custom watcher:
1. Create a `watchers/[watcher_name].py` file which defines a `Watcher` class with a `run()` method
2. Your `run()` method should run continuously (loop, event listener) and require no parameters
3. If you need any additional configuration parameters, make sure to update `config.yaml.example`
4. If adding any generic or reusable functionality, consider moving it to `watchers/helpers/`
5. Update the `watchers/README.md` with a brief description and any useful instructions

Take inspiration from existing watchers and submit a pull request for code review.
