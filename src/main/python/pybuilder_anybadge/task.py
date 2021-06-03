#   -*- coding: utf-8 -*-
import os
import re
import sys
import json
from pybuilder.core import init
from pybuilder.core import task
from pybuilder.core import depends

from anybadge import Badge

URL = {
    'complexity': 'https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity',
    'vulnerabilities': 'https://pypi.org/project/bandit/',
    'python': 'https://www.python.org/downloads/'
}


@init
def init_anybadge(project):
    """ initialize anybadge task
    """
    project.plugin_depends_on('anybadge')
    project.set_property_if_unset('anybadge_exclude', [])
    project.set_property_if_unset('anybadge_complexity_use_average', False)
    project.set_property_if_unset('anybadge_use_shields', False)


@task('anybadge', description='generate badges from reports using anybadge')
@depends('prepare')
def anybadge(project, logger, reactor):
    """ generate badges from reports using anybadge
    """
    reports_directory = project.expand_path('$dir_reports')
    images_directory = get_images_directory(project)
    use_shields = project.get_property('anybadge_use_shields')
    exclude = get_badge_exclude(project)
    logger.debug(f'task instructed to exclude {exclude}')
    if 'python' not in exclude:
        badge_path = os.path.join(images_directory, 'python.svg')
        create_python_badge(badge_path, logger, use_shields=use_shields)
    if 'vulnerabilities' not in exclude:
        report_path = os.path.join(reports_directory, 'bandit.json')
        badge_path = os.path.join(images_directory, 'vulnerabilities.svg')
        create_vulnerabilities_badge(report_path, badge_path, logger, use_shields=use_shields)
    if 'complexity' not in exclude:
        report_path = os.path.join(reports_directory, 'radon')
        badge_path = os.path.join(images_directory, 'complexity.svg')
        use_average = project.get_property('anybadge_complexity_use_average')
        create_complexity_badge(report_path, badge_path, logger, use_average, use_shields=use_shields)
    if 'coverage' not in exclude:
        report_path = os.path.join(reports_directory, f'{project.name}_coverage.json')
        badge_path = os.path.join(images_directory, 'coverage.svg')
        create_coverage_badge(report_path, badge_path, logger, use_shields=use_shields)


def get_images_directory(project):
    """ return images directory and create directory if does not already exist
    """
    images_directory = os.path.join(project.basedir, 'docs', 'images')
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
    return images_directory


def get_badge_exclude(project):
    """ return list of badges to exclude
    """
    exclusions = []
    exclude = project.get_property('anybadge_exclude')
    if exclude:
        exclusions = [item.strip() for item in exclude.split(',')]
    return exclusions


def accessible(filename):
    """ return True if filename is file and current context has read access otherwise False
    """
    return os.path.isfile(filename) and os.access(filename, os.R_OK)


def read_lines(filename):
    """ return content of filename as list of lines
    """
    with open(filename) as infile:
        return infile.readlines()


def read_data(filename):
    """ return dictionary read from json file
    """
    with open(filename) as infile:
        return json.load(infile)


def get_complexity_report(lines):
    """ return complexity report by analyzing lines
    """
    report = {
        'average': None,
        'highest': {
            'name': None,
            'score': 0
        }
    }
    regex_score = r'[A-Z] \d+:\d+ (?P<name>.*) - [A-Z] \((?P<score>\d+)\)'
    for line in lines[:-1]:
        line = line.strip()
        match = re.match(regex_score, line)
        if match:
            score = round(float(match.group('score')))
            if score > report['highest']['score']:
                report['highest']['score'] = score
                report['highest']['name'] = match.group('name')

    last_line = lines[-1].strip()
    regex_average = r'Average complexity: [A-Z] \((?P<average>.*)\)'
    match_average = re.match(regex_average, last_line)
    if match_average:
        average = match_average.group('average')
        report['average'] = round(float(average), 2)

    return report


def get_complexity_badge(complexity_report, use_average=False, use_shields=False):
    """ return complexity badge based off of complexity_report
        https://radon.readthedocs.io/en/latest/api.html#radon.complexity.cc_rank
        1  - 5  : Simple   - BrightGreen
        6  - 10 : Stable   - Olive
        11 - 20 : Slight   - Yellow
        21 - 30 : Complex  - Orange
        31 - 40 : Alarming - Red
        40+     : Unstable - BrightRed
    """
    score = complexity_report['highest']['score']
    if use_average:
        score = complexity_report['average']

    if score <= 5:
        value = 'Simple'
        if use_shields:
            color = 'brightgreen'
        else:
            color = 'green'
    elif score <= 10:
        value = 'Stable'
        color = 'olive'
    elif score <= 20:
        value = 'Slight'
        color = 'yellow'
    elif score <= 30:
        value = 'Complex'
        color = 'orange'
    elif score <= 40:
        value = 'Alarming'
        color = 'red'
    else:
        value = 'Unstable'
        color = 'brightred'

    if use_shields:
        badge = f'https://img.shields.io/badge/complexity-{value}: {score}-{color}'
        badge = badge.replace(' ', '%20')
    else:
        badge = Badge('complexity', value=f'{value}: {score}', default_color=color)
    return badge


def get_vulnerabilities_badge(vulnerabilities_report, use_shields=False):
    """ return vulnerabilities badge based off of vulnerabilities_report
        High      - Red
        Medium    - Orange
        Low       - Yellow
        Undefined - Gray
        None      - BrightGreen
    """
    if use_shields:
        color = 'brightgreen'
    else:
        color = 'green'
    value = 'None'

    metrics = vulnerabilities_report['metrics']['_totals']
    if metrics['SEVERITY.UNDEFINED'] > 0:
        color = 'gray'
        value = 'Undefined'
    if metrics['SEVERITY.LOW'] > 0:
        color = 'yellow'
        value = 'Low'
    if metrics['SEVERITY.MEDIUM'] > 0:
        color = 'orange'
        value = 'Medium'
    if metrics['SEVERITY.HIGH'] > 0:
        color = 'red'
        value = 'High'

    if use_shields:
        badge = f'https://img.shields.io/badge/vulnerabilities-{value}-{color}'
    else:
        badge = Badge('vulnerabilities', value=value, default_color=color)
    return badge


def get_coverage(coverage_data):
    """ return coverage from coveage lines
    """
    if len(coverage_data['module_names']) == 0:
        return 0
    return coverage_data['overall_coverage']


def get_coverage_badge(coverage, use_shields=False):
    """ return coverage badge based off of coverage report
    """
    if use_shields:
        color = 'brightgreen'
    else:
        color = 'green'
    if coverage < 85:
        color = 'yellow'
    if coverage < 70:
        color = 'orange'
    if coverage < 55:
        color = 'red'
    value = f'{round(coverage, 2)}%'
    if use_shields:
        badge = f'https://img.shields.io/badge/coverage-{value}-{color}'
        badge = badge.replace('%', '%25')
    else:
        badge = Badge('coverage', value=value, default_color=color)
    return badge


def get_python_badge(use_shields=False):
    """ return badge for python version
    """
    value = f'{sys.version_info.major}.{sys.version_info.minor}'
    color = 'teal'
    if use_shields:
        badge = f'https://img.shields.io/badge/python-{value}-{color}'
    else:
        badge = Badge('python', value=value, default_color=color)
    return badge


def update_readme(line_to_add, logger):
    """ add badge to readme
    """
    filename = 'README.md'
    if not accessible(filename):
        logger.warn(f'{filename} does not exist or is not accessible')
        return

    with open('README.md', 'r+') as file_handler:
        lines = file_handler.readlines()
        for line in lines:
            if line.startswith(line_to_add):
                logger.debug(f'{filename} already contains {line_to_add.strip()}')
                break
        else:
            file_handler.seek(0)
            lines.insert(0, line_to_add)
            file_handler.writelines(lines)


def get_line_to_add(name, badge, badge_is_url):
    """ return line to add in markdown
    """
    url = URL.get(name, 'https://pybuilder.io/')
    if badge_is_url:
        line_to_add = f"[![{name}]({badge})]({url})\n"
    else:
        relative_path = os.path.join('docs', 'images', os.path.basename(badge))
        line_to_add = f"[![{name}]({relative_path})]({url})\n"
    return line_to_add


def create_complexity_badge(report_path, badge_path, logger, use_average, use_shields=False):
    """ create complexity badge from radon report
    """
    if accessible(report_path):
        complexity_data = get_complexity_report(read_lines(report_path))
        badge = get_complexity_badge(complexity_data, use_average=use_average, use_shields=use_shields)
        if use_shields:
            line_to_add = get_line_to_add('complexity', badge, use_shields)
        else:
            badge.write_badge(badge_path, overwrite=True)
            line_to_add = get_line_to_add('complexity', badge_path, use_shields)
        update_readme(line_to_add, logger)
    else:
        logger.warn(f'{report_path} is not accessible')


def create_vulnerabilities_badge(report_path, badge_path, logger, use_shields=False):
    """ create vulnerabilities badge from bandit report
    """
    if accessible(report_path):
        vulnerabilities_data = read_data(report_path)
        badge = get_vulnerabilities_badge(vulnerabilities_data, use_shields=use_shields)
        if use_shields:
            line_to_add = get_line_to_add('vulnerabilities', badge, use_shields)
        else:
            badge.write_badge(badge_path, overwrite=True)
            line_to_add = get_line_to_add('vulnerabilities', badge_path, use_shields)
        update_readme(line_to_add, logger)
    else:
        logger.warn(f'{report_path} is not accessible')


def create_coverage_badge(report_path, badge_path, logger, use_shields=False):
    """ create coverage badge from coverage report
    """
    if accessible(report_path):
        coverage_data = get_coverage(read_data(report_path))
        badge = get_coverage_badge(coverage_data, use_shields=use_shields)
        if use_shields:
            line_to_add = get_line_to_add('coverage', badge, use_shields)
        else:
            badge.write_badge(badge_path, overwrite=True)
            line_to_add = get_line_to_add('coverage', badge_path, use_shields)
        update_readme(line_to_add, logger)
    else:
        logger.warn(f'{report_path} is not accessible')


def create_python_badge(badge_path, logger, use_shields=False):
    """ create python version badge
    """
    badge = get_python_badge(use_shields=use_shields)
    if use_shields:
        line_to_add = get_line_to_add('python', badge, use_shields)
    else:
        badge.write_badge(badge_path, overwrite=True)
        line_to_add = get_line_to_add('python', badge_path, use_shields)
    update_readme(line_to_add, logger)
