# pybuilder-anybadge
[![GitHub Workflow Status](https://github.com/soda480/pybuilder-anybadge/workflows/build/badge.svg)](https://github.com/soda480/pybuilder-anybadge/actions)
[![Code Coverage](https://codecov.io/gh/soda480/pybuilder-anybadge/branch/main/graph/badge.svg)](https://codecov.io/gh/soda480/pybuilder-anybadge)
[![Code Grade](https://api.codiga.io/project/20103/status/svg)](https://app.codiga.io/public/project/20103/pybuilder-anybadge/dashboard)
[![PyPI version](https://badge.fury.io/py/pybuilder-anybadge.svg)](https://badge.fury.io/py/pybuilder-anybadge)
[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)

A pybuilder plugin that generates badges for your project. The plugin by default will create badges using `anybadge`, for more information refer to the [anybadge pypi page](https://pypi.org/project/anybadge/). The plugin can also be configured to generate the badges using `img.shields.io`.

To add this plugin into your pybuilder project, add the following line near the top of your build.py:
```python
use_plugin('pypi:pybuilder_anybadge')
```

**NOTE** if you are using Pybuilder version `v0.11.x`, then specify the following version of the plugin:
```python
use_plugin('pypi:pybuilder_anybadge', '~=0.1.6')
```

### Pybuilder anybadge properties

The pybuilder task `pyb anybadge` will use anybadge to generate badges for your project by processing reports produced from various plugins; the badges that are currently supported are:
- **complexity** - requires the [pybuilder_radon](https://pypi.org/project/pybuilder-radon/) plugin. Generate badge using cyclomatic complexity score of your most complicated function.
- **vulnerabilities** - requires the [pybuilder_bandit](https://pypi.org/project/pybuilder-bandit/) plugin. Generate badge using number of security vulnerabilities discovered by vulnerabilities.
- **coverage** - requires the `coverage` plugin. Generate badge for overall unit test coverage.
- **python** - Generate badge for version of Python being used

The plugin will write the respective badges to the `docs/images` folder. The following plugin properties are available to further configure badge generation.

Name | Type | Default Value | Description
-- | -- | -- | --
anybadge_exclude | str | '' | Comma delimited string of badges to exclude from processing, valid values are 'complexity', 'vulnerabilities', 'coverage' and 'python'
anybadge_complexity_use_average | bool | False | Use overall average complexity as score when generating complexity badge
anybadge_use_shields | bool | False | Will use `img.shields.io` to create the badges instead of `anybadge`

**Note** the plugin will add the badge references but you must commit/push the changes (including svg files in the docs/images folder)

The plugin properties are set using `project.set_property`, the following is an example of how to set the properties:

```Python
project.set_property('anybadge_exclude', 'vulnerabilities,coverage')
project.set_property('anybadge_complexity_use_average', True)
project.set_property('anybadge_use_shields', False)
```

By default the plugin will use `anybadge` to create the badges and save them as svg files in the `docs\images` folder:

![coverage](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/coverage.svg)
![complexity](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/complexity.svg)
![vulnerabilities](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/vulnerabilities.svg)
![python](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/python.svg)

However, setting `anybadge_use_shields` to `True` will render the badges using `img.shields.io`:

[![coverage](https://img.shields.io/badge/coverage-100.0%25-brightgreen)](https://pybuilder.io/)
[![complexity](https://img.shields.io/badge/complexity-Stable:%209-olive)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)
[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)
[![python](https://img.shields.io/badge/python-3.6-teal)](https://www.python.org/downloads/)

### Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t \
pybanybadge:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/code \
pybanybadge:latest \
bash
```

Execute the build:
```sh
pyb -X
```
