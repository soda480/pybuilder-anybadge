#   -*- coding: utf-8 -*-
import os
import re
import json
from pybuilder.core import init
from pybuilder.core import task
from pybuilder.core import depends

from anybadge import Badge


@init
def init_anybadge(project):
    """ initialize anybadge task
    """
    project.plugin_depends_on('anybadge')
    project.set_property_if_unset('anybadge_exclude', [])
    project.set_property_if_unset('anybadge_add_to_readme', False)


@task('anybadge', description='generate badges from reports using anybadge')
@depends('prepare')
def anybadge(project, logger):
    """ generate badges from reports using anybadge
    """
    reports_directory = project.expand_path('$dir_reports')
    images_directory = get_images_directory(project)
    add_to_readme = project.get_property('anybadge_add_to_readme')
    exclude = get_badge_exclude(project)
    logger.debug(f'task instructed to exclude {exclude}')
    if 'complexity' not in exclude:
        create_complexity_badge(f'{reports_directory}/radon', f'{images_directory}/complexity.svg', logger, add_to_readme)
    if 'severity' not in exclude:
        create_severity_badge(f'{reports_directory}/bandit.json', f'{images_directory}/severity.svg', logger, add_to_readme)
    if 'coverage' not in exclude:
        create_coverage_badge(f'{reports_directory}/coverage', f'{images_directory}/coverage.svg', logger, add_to_readme)


def get_images_directory(project):
    """ return images directory and create directory if does not already exist
    """
    target_directory = project.expand_path('$dir_target')
    images_directory = target_directory.replace('/target', '/docs/images')
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
    return images_directory


def get_badge_exclude(project):
    """ return list of badges to exclude
    """
    exclude = project.get_property('anybadge_exclude')
    if exclude:
        return exclude.split(',')
    return []


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
            score = float(match.group('score'))
            if score > report['highest']['score']:
                report['highest']['score'] = score
                report['highest']['name'] = match.group('name')

    last_line = lines[-1].strip()
    regex_average = r'Average complexity: [A-Z] \((?P<average>.*)\)'
    match = re.match(regex_average, last_line)
    if match:
        report['average'] = float(match.group('average'))

    return report


def get_complexity_badge(complexity_report, use_average=False):
    """ return complexity badge based off of complexity_report
        https://radon.readthedocs.io/en/latest/api.html#radon.complexity.cc_rank
        1  - 5  : Simple   - Green
        6  - 10 : Stable   - Green
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
        color = 'green'
    elif score <= 10:
        value = 'Stable'
        color = 'green'
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

    return Badge('complexity', value=value, default_color=color, num_padding_chars=1)


def get_severity_badge(severity_report):
    """ return severity badge based off of severity_report
        High      - Red
        Medium    - Orange
        Low       - Yellow
        Undefined - Gray
        None      - Green
    """
    color = 'green'
    value = 'None'

    metrics = severity_report['metrics']['_totals']
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

    return Badge('severity', value=value, default_color=color, num_padding_chars=1)


def get_coverage(coverage_lines):
    """ return coverage from coveage lines
    """
    total_line = coverage_lines[-1].strip()
    regex = r'^TOTAL.* (?P<coverage>\d+)%$'
    match = re.match(regex, total_line)
    if match:
        return int(match.group('coverage'))


def get_coverage_badge(coverage):
    """ return coverage badge based off of coverage report
    """
    color = 'green'
    if coverage < 85:
        color = 'yellow'
    if coverage < 70:
        color = 'orange'
    if coverage < 55:
        color = 'red'
    value = f'{coverage}%'
    return Badge('coverage', value=value, default_color=color, num_padding_chars=1)


def update_readme(name, badge_filename, add_to_readme, logger):
    """ add badge to readme
    """
    if not add_to_readme:
        return
    filename = 'README.md'
    if not accessible(filename):
        logger.warn(f'{filename} does not exist or is not accessible')
        return
    # not super clean but is the best we can do for now
    relative_filename = f"docs/images{badge_filename.split('/docs/images')[1]}"
    line_to_add = f'![{name}]({relative_filename})\n'
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


def create_complexity_badge(report_filename, badge_filename, logger, add_to_readme):
    """ create complexity badge from radon report
    """
    if not accessible(report_filename):
        logger.warn(f'{report_filename} does not exist or is not accessible')
        return
    lines = read_lines(report_filename)
    report = get_complexity_report(lines)
    badge = get_complexity_badge(report)
    logger.info(f'writing complexity badge {badge_filename}')
    badge.write_badge(badge_filename, overwrite=True)
    update_readme('complexity', badge_filename, add_to_readme, logger)


def create_severity_badge(report_filename, badge_filename, logger, add_to_readme):
    """ create severity badge from bandit report
    """
    if not accessible(report_filename):
        logger.warn(f'{report_filename} does not exist or is not accessible')
        return
    severity_report = read_data(report_filename)
    badge = get_severity_badge(severity_report)
    logger.info(f'writing severity badge {badge_filename}')
    badge.write_badge(badge_filename, overwrite=True)
    update_readme('severity', badge_filename, add_to_readme, logger)


def create_coverage_badge(report_filename, badge_filename, logger, add_to_readme):
    """ create coverage badge from coverage report
    """
    if not accessible(report_filename):
        logger.warn(f'{report_filename} does not exist or is not accessible')
        return
    lines = read_lines(report_filename)
    coverage = get_coverage(lines)
    if coverage is None:
        logger.warn(f'unable to extract coverage data from: {report_filename}')
        return
    badge = get_coverage_badge(coverage)
    logger.info(f'writing coverage badge {badge_filename}')
    badge.write_badge(badge_filename, overwrite=True)
    update_readme('coverage', badge_filename, add_to_readme, logger)
