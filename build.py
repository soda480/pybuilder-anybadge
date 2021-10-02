#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin
from pybuilder.core import init
from pybuilder.core import Author

# only for functional testing plugin
# from pybuilder_anybadge import anybadge

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.install_dependencies')
use_plugin('python.flake8')
use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('pypi:pybuilder_radon')
use_plugin('pypi:pybuilder_bandit')


name = 'pybuilder-anybadge'
authors = [Author('Emilio Reyes', 'soda480@gmail.com')]
summary = 'A pybuilder plugin that generates badges for your project'
url = 'https://github.com/soda480/pybuilder-anybadge'
version = '0.3.0'
default_task = [
    'clean',
    'radon',
    'bandit',
    'publish'
]
license = 'Apache License, Version 2.0'
description = summary


@init
def set_properties(project):
    project.set_property('unittest_module_glob', 'test_*.py')
    project.set_property('coverage_break_build', False)
    project.set_property('flake8_max_line_length', 120)
    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)
    project.set_property('flake8_include_scripts', True)
    project.set_property('flake8_include_test_sources', True)
    project.set_property('flake8_ignore', 'F401, E501, E722')
    project.build_depends_on_requirements('requirements-build.txt')
    project.depends_on_requirements('requirements.txt')
    project.set_property('distutils_readme_description', True)
    project.set_property('distutils_description_overwrite', True)
    project.set_property('distutils_upload_skip_existing', True)
    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Build Tools'])
    # only for functional testing plugin
    # project.set_property('anybadge_exclude', 'vulnerabilities, coverage')
    # project.set_property('anybadge_complexity_use_average', True)
    # project.set_property('anybadge_use_shields', True)
