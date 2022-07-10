#   -*- coding: utf-8 -*-
import unittest
from mock import patch
from mock import call
from mock import Mock
from mock import mock_open

from pybuilder_anybadge.task import init_anybadge
from pybuilder_anybadge.task import anybadge
from pybuilder_anybadge.task import get_images_directory
from pybuilder_anybadge.task import get_badge_exclude
from pybuilder_anybadge.task import accessible
from pybuilder_anybadge.task import read_lines
from pybuilder_anybadge.task import read_data
from pybuilder_anybadge.task import get_complexity_report
from pybuilder_anybadge.task import get_complexity_badge
from pybuilder_anybadge.task import get_vulnerabilities_badge
from pybuilder_anybadge.task import get_coverage
from pybuilder_anybadge.task import get_coverage_badge
from pybuilder_anybadge.task import get_python_badge
from pybuilder_anybadge.task import update_readme
from pybuilder_anybadge.task import get_line_to_add
from pybuilder_anybadge.task import create_complexity_badge
from pybuilder_anybadge.task import create_vulnerabilities_badge
from pybuilder_anybadge.task import create_coverage_badge
from pybuilder_anybadge.task import create_python_badge
from pybuilder_anybadge.task import get_python_version
from pybuilder_anybadge.task import URL


class TestTask(unittest.TestCase):

    def test__init_anybadge_Should_CallExpected_When_Called(self, *patches):
        project_mock = Mock()
        init_anybadge(project_mock)
        self.assertTrue(call('anybadge_exclude', []) in project_mock.set_property_if_unset.mock_calls)
        self.assertTrue(call('anybadge_use_shields', False) in project_mock.set_property_if_unset.mock_calls)

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_python_badge')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_vulnerabilities_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeComplexity(self, get_badge_exclude_patch, create_complexity_badge_patch, create_vulnerabilities_badge_patch, create_coverage_badge_patch, create_python_badge_patch, get_images_directory_patch, *patches):
        get_images_directory_patch.return_value = '/project/docs/images'
        get_badge_exclude_patch.return_value = ['complexity']
        project_mock = Mock()
        project_mock.expand_path.return_value = '/project/dir/reports'
        project_mock.get_property.side_effect = [False]
        logger_mock = Mock()
        anybadge(project_mock, logger_mock, Mock())
        create_complexity_badge_patch.assert_not_called()
        create_vulnerabilities_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/bandit.json', f'{get_images_directory_patch.return_value}/vulnerabilities.svg', logger_mock, use_shields=False)
        create_coverage_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/{project_mock.name}_coverage.json', f'{get_images_directory_patch.return_value}/coverage.svg', logger_mock, use_shields=False)
        create_python_badge_patch.assert_called_once_with(project_mock, f'{get_images_directory_patch.return_value}/python.svg', logger_mock, use_shields=False)

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_python_badge')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_vulnerabilities_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeSeverity(self, get_badge_exclude_patch, create_complexity_badge_patch, create_vulnerabilities_badge_patch, create_coverage_badge_patch, create_python_badge_patch, get_images_directory_patch, *patches):
        get_images_directory_patch.return_value = '/project/docs/images'
        get_badge_exclude_patch.return_value = ['vulnerabilities']
        project_mock = Mock()
        project_mock.get_property.side_effect = [False, True]
        project_mock.expand_path.return_value = '/project/dir/reports'
        logger_mock = Mock()
        anybadge(project_mock, logger_mock, Mock())
        create_complexity_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/radon', f'{get_images_directory_patch.return_value}/complexity.svg', logger_mock, True, use_shields=False)
        create_vulnerabilities_badge_patch.assert_not_called()
        create_coverage_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/{project_mock.name}_coverage.json', f'{get_images_directory_patch.return_value}/coverage.svg', logger_mock, use_shields=False)
        create_python_badge_patch.assert_called_once_with(project_mock, f'{get_images_directory_patch.return_value}/python.svg', logger_mock, use_shields=False)

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_python_badge')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_vulnerabilities_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeCoverage(self, get_badge_exclude_patch, create_complexity_badge_patch, create_vulnerabilities_badge_patch, create_coverage_badge_patch, create_python_badge_patch, get_images_directory_patch, *patches):
        get_images_directory_patch.return_value = '/project/docs/images'
        get_badge_exclude_patch.return_value = ['coverage']
        project_mock = Mock()
        project_mock.get_property.side_effect = [False, False]
        project_mock.expand_path.return_value = '/project/dir/reports'
        logger_mock = Mock()
        anybadge(project_mock, logger_mock, Mock())
        create_complexity_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/radon', f'{get_images_directory_patch.return_value}/complexity.svg', logger_mock, False, use_shields=False)
        create_vulnerabilities_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/bandit.json', f'{get_images_directory_patch.return_value}/vulnerabilities.svg', logger_mock, use_shields=False)
        create_coverage_badge_patch.assert_not_called()
        create_python_badge_patch.assert_called_once_with(project_mock, f'{get_images_directory_patch.return_value}/python.svg', logger_mock, use_shields=False)

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_python_badge')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_vulnerabilities_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludePython(self, get_badge_exclude_patch, create_complexity_badge_patch, create_vulnerabilities_badge_patch, create_coverage_badge_patch, create_python_badge_patch, get_images_directory_patch, *patches):
        get_images_directory_patch.return_value = '/project/docs/images'
        get_badge_exclude_patch.return_value = ['python']
        project_mock = Mock()
        project_mock.get_property.side_effect = [False, False]
        project_mock.expand_path.return_value = '/project/dir/reports'
        logger_mock = Mock()
        anybadge(project_mock, logger_mock, Mock())
        create_complexity_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/radon', f'{get_images_directory_patch.return_value}/complexity.svg', logger_mock, False, use_shields=False)
        create_vulnerabilities_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/bandit.json', f'{get_images_directory_patch.return_value}/vulnerabilities.svg', logger_mock, use_shields=False)
        create_coverage_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/{project_mock.name}_coverage.json', f'{get_images_directory_patch.return_value}/coverage.svg', logger_mock, use_shields=False)
        create_python_badge_patch.assert_not_called()

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_python_badge')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_vulnerabilities_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeAll(self, get_badge_exclude_patch, create_complexity_badge_patch, create_vulnerabilities_badge_patch, create_coverage_badge_patch, create_python_badge_patch, *patches):
        get_badge_exclude_patch.return_value = ['coverage', 'vulnerabilities', 'complexity', 'python']
        project_mock = Mock()
        logger_mock = Mock()
        anybadge(project_mock, logger_mock, Mock())
        create_complexity_badge_patch.assert_not_called()
        create_vulnerabilities_badge_patch.assert_not_called()
        create_coverage_badge_patch.assert_not_called()
        create_python_badge_patch.assert_not_called()

    @patch('pybuilder_anybadge.task.os.path.exists', return_value=False)
    @patch('pybuilder_anybadge.task.os.makedirs')
    def test__get_images_directory_Should_CallAndReturnExpected_When_ImagesDirectoryDoesNotExist(self, makedirs_patch, *patches):
        project_mock = Mock()
        project_mock.basedir = '/project'
        result = get_images_directory(project_mock)
        expected_result = '/project/docs/images'
        makedirs_patch.assert_called_once_with(expected_result)
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.os.path.exists', return_value=True)
    @patch('pybuilder_anybadge.task.os.makedirs')
    def test__get_images_directory_Should_CallAndReturnExpected_When_ImagesDirectoryDoesExist(self, makedirs_patch, *patches):
        project_mock = Mock()
        project_mock.basedir = '/project'
        result = get_images_directory(project_mock)
        expected_result = '/project/docs/images'
        makedirs_patch.assert_not_called()
        self.assertEqual(result, expected_result)

    def test__get_badge_exclude_Should_ReturnExpected_When_Exclude(self, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = ' item1,  item2,item3,      item4'
        result = get_badge_exclude(project_mock)
        expected_result = ['item1', 'item2', 'item3', 'item4']
        self.assertEqual(result, expected_result)

    def test__get_badge_exclude_Should_ReturnExpected_When_NoExclude(self, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = None
        result = get_badge_exclude(project_mock)
        expected_result = []
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.os.access', return_value=True)
    @patch('pybuilder_anybadge.task.os.path.isfile', return_value=True)
    def test__accessible_Should_ReturnTrue_When_Expected(self, *patches):

        self.assertTrue(accessible('--filename--'))

    @patch('pybuilder_anybadge.task.os.access', return_value=True)
    @patch('pybuilder_anybadge.task.os.path.isfile', return_value=False)
    def test__accessible_Should_ReturnFalse_When_Expected(self, *patches):

        self.assertFalse(accessible('--filename--'))

    @patch('pybuilder_anybadge.task.open', create=True)
    def test__read_lines_Should_ReturnExpected_When_Called(self, open_patch, *patches):
        open_patch.side_effect = [
            mock_open(read_data='--data--').return_value
        ]
        read_lines('--filename--')

    @patch('pybuilder_anybadge.task.open', create=True)
    @patch('pybuilder_anybadge.task.json')
    def test__read_data_Should_ReturnExpected_When_Called(self, json_patch, open_patch, *patches):
        open_patch.side_effect = [
            mock_open(read_data='--data--').return_value
        ]
        result = read_data('--filename--')
        self.assertEqual(result, json_patch.load.return_value)

    def test__get_complexity_report_Should_ReturnExpected_When_CalledNoVerbose(self, *patches):
        report_lines = [
            '\n',
            '    M 81:4 class.ma - C (14)\n',
            '    M 231:4 class.mb - A (4)\n',
            'src/main/python/package/module.py\n',
            '    C 40:0 class.mc - B (9)\n',
            '\n',
            'Average complexity: A (3.557377049180328)']
        result = get_complexity_report(report_lines)
        expected_result = {
            'average': 3.56,
            'highest': {
                'name': 'class.ma',
                'score': 14
            }
        }
        self.assertEqual(result, expected_result)

    def test__get_complexity_report_Should_ReturnExpected_When_NoMatch(self, *patches):
        report_lines = [
            '\n',
            '    M 81:4 class.ma -\n',
            '    M 231:4 class.mb -\n',
            'src/main/python/package/module.py\n',
            '    C 40:0 class.mc -\n',
            '\n',
            'Average complexity:)']
        result = get_complexity_report(report_lines)
        expected_result = {
            'average': None,
            'highest': {
                'name': None,
                'score': 0
            }
        }
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_SimpleGreen(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 5
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Simple: 5', default_color='green')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_StableGreen(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 10
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Stable: 10', default_color='olive')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_SlightYellow(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 20
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Slight: 20', default_color='yellow')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_ComplexOrange(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 30
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Complex: 30', default_color='orange')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_AlarmingRed(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 40
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Alarming: 40', default_color='red')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_UnstableBrightred(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 50
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Unstable: 50', default_color='brightred')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_UseAverage(self, badge_patch, *patches):
        complexity_report = {
            'average': 79,
            'highest': {
                'score': 50
            }
        }
        result = get_complexity_badge(complexity_report, use_average=True)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Unstable: 79', default_color='brightred')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_UseShields(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 5
            }
        }
        result = get_complexity_badge(complexity_report, use_shields=True)
        expected_result = 'https://img.shields.io/badge/complexity-Simple:%205-brightgreen'
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_vulnerabilities_badge_Should_ReturnExpected_When_GrayUndefined(self, badge_patch, *patches):
        vulnerabilities_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 1.0,
                    'SEVERITY.LOW': 0.0,
                    'SEVERITY.MEDIUM': 0.0,
                    'SEVERITY.HIGH': 0.0,
                }
            }
        }
        result = get_vulnerabilities_badge(vulnerabilities_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('vulnerabilities', value='Undefined', default_color='gray')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_vulnerabilities_badge_Should_ReturnExpected_When_LowYellow(self, badge_patch, *patches):
        vulnerabilities_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 0.0,
                    'SEVERITY.LOW': 1.0,
                    'SEVERITY.MEDIUM': 0.0,
                    'SEVERITY.HIGH': 0.0,
                }
            }
        }
        result = get_vulnerabilities_badge(vulnerabilities_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('vulnerabilities', value='Low', default_color='yellow')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_vulnerabilities_badge_Should_ReturnExpected_When_MediumOrange(self, badge_patch, *patches):
        vulnerabilities_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 0.0,
                    'SEVERITY.LOW': 0.0,
                    'SEVERITY.MEDIUM': 1.0,
                    'SEVERITY.HIGH': 0.0,
                }
            }
        }
        result = get_vulnerabilities_badge(vulnerabilities_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('vulnerabilities', value='Medium', default_color='orange')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_vulnerabilities_badge_Should_ReturnExpected_When_HighRed(self, badge_patch, *patches):
        vulnerabilities_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 1.0,
                    'SEVERITY.LOW': 1.0,
                    'SEVERITY.MEDIUM': 1.0,
                    'SEVERITY.HIGH': 1.0,
                }
            }
        }
        result = get_vulnerabilities_badge(vulnerabilities_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('vulnerabilities', value='High', default_color='red')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_vulnerabilities_badge_Should_ReturnExpected_When_UseShields(self, badge_patch, *patches):
        vulnerabilities_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 1.0,
                    'SEVERITY.LOW': 1.0,
                    'SEVERITY.MEDIUM': 1.0,
                    'SEVERITY.HIGH': 1.0,
                }
            }
        }
        result = get_vulnerabilities_badge(vulnerabilities_report, use_shields=True)
        expected_result = 'https://img.shields.io/badge/vulnerabilities-High-red'
        self.assertEqual(result, expected_result)

    def test__get_coverage_Should_Return_Expected_When_NoModuleNames(self, *patches):
        coverage_data = {
            'module_names': [],
        }
        result = get_coverage(coverage_data)
        self.assertEqual(result, len(coverage_data['module_names']))

    def test__get_coverage_Should_Return_Expected_When_ModuleNames(self, *patches):
        coverage_data = {
            'module_names': ['--module1--', '--module2--'],
            'overall_coverage': 45.0
        }
        result = get_coverage(coverage_data)
        self.assertEqual(result, coverage_data['overall_coverage'])

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Green(self, badge_patch, *patches):
        result = get_coverage_badge(100)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='100%', default_color='green')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Yellow(self, badge_patch, *patches):
        result = get_coverage_badge(84.234342342343)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='84.23%', default_color='yellow')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Orange(self, badge_patch, *patches):
        result = get_coverage_badge(69.13933332232)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='69.14%', default_color='orange')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Red(self, badge_patch, *patches):
        result = get_coverage_badge(54)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='54%', default_color='red')

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_UseShields(self, badge_patch, *patches):
        result = get_coverage_badge(54, use_shields=True)
        expected_result = 'https://img.shields.io/badge/coverage-54%25-red'
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.get_python_version', return_value='--major--.--minor--')
    @patch('pybuilder_anybadge.task.Badge')
    def test__get_python_badge_Should_ReturnExpected_When_Called(self, badge_patch, *patches):
        project_mock = Mock()
        result = get_python_badge(project_mock)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('python', value='--major--.--minor--', default_color='teal')

    @patch('pybuilder_anybadge.task.get_python_version', return_value='3.6')
    @patch('pybuilder_anybadge.task.Badge')
    def test__get_python_badge_Should_ReturnExpected_When_UseShields(self, badge_patch, *patches):
        project_mock = Mock()
        result = get_python_badge(project_mock, use_shields=True)
        expected_result = 'https://img.shields.io/badge/python-3.6-teal'
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.accessible', return_value=False)
    def test__update_readme_Should_CallExpected_When_NotAccessible(self, *patches):
        logger_mock = Mock()
        update_readme('--line-to-add--', logger_mock)
        logger_mock.warn.assert_called()

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.open', create=True)
    def test__update_readme_Should_CallExpected_When_NoMatch(self, open_patch, *patches):
        open_patch.side_effect = [
            mock_open(read_data='line1\nline2\nline3').return_value
        ]
        logger_mock = Mock()
        update_readme('line4', logger_mock)

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.open', create=True)
    def test__update_readme_Should_CallExpected_When_Match(self, open_patch, *patches):
        open_patch.side_effect = [
            mock_open(read_data='line1\nline2\nline3').return_value
        ]
        logger_mock = Mock()
        update_readme('line2', logger_mock)

    def test__get_line_to_add_Should_ReturnExpected_When_BadgeIsUrl(self, *patches):
        name = 'vulnerabilities'
        badge = 'badge-url'
        url = URL.get(name)
        result = get_line_to_add(name, badge, True)
        expected_result = f"[![{name}]({badge})]({url})\n"
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.os.path.basename')
    @patch('pybuilder_anybadge.task.os.path.join')
    def test__get_line_to_add_Should_ReturnExpected_When_NotBadgeIsUrl(self, join_patch, *patches):
        name = 'vulnerabilities'
        badge = 'badge-url'
        url = URL.get(name)
        relative_path = join_patch.return_value
        result = get_line_to_add(name, badge, False)
        expected_result = f"[![{name}]({relative_path})]({url})\n"
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.accessible', return_value=False)
    def test__create_complexity_badge_Should_CallExpected_When_NotAccessible(self, *patches):
        logger_mock = Mock()
        create_complexity_badge('--report-filename--', '--badge-filename--', logger_mock, True)
        logger_mock.warn.assert_called()

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.read_lines')
    @patch('pybuilder_anybadge.task.get_complexity_report')
    @patch('pybuilder_anybadge.task.get_complexity_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_complexity_badge_Should_CallExpected_When_Accessible(self, update_readme_patch, get_line_to_add_patch, *patches):
        logger_mock = Mock()
        create_complexity_badge('--report-filename--', '--badge-filename--', logger_mock, True)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.read_lines')
    @patch('pybuilder_anybadge.task.get_complexity_report')
    @patch('pybuilder_anybadge.task.get_complexity_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_complexity_badge_Should_CallExpected_When_UseShields(self, update_readme_patch, get_line_to_add_patch, *patches):
        logger_mock = Mock()
        create_complexity_badge('--report-filename--', '--badge-filename--', logger_mock, True, use_shields=True)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)

    @patch('pybuilder_anybadge.task.accessible', return_value=False)
    def test__create_vulnerabilities_badge_Should_CallExpected_When_NotAccessible(self, *patches):
        logger_mock = Mock()
        create_vulnerabilities_badge('--report-filename--', '--badge-filename--', logger_mock)
        logger_mock.warn.assert_called()

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.read_data')
    @patch('pybuilder_anybadge.task.get_vulnerabilities_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_vulnerabilities_badge_Should_CallExpected_When_Accessible(self, update_readme_patch, get_line_to_add_patch, *patches):
        logger_mock = Mock()
        create_vulnerabilities_badge('--report-filename--', '--badge-filename--', logger_mock)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.read_data')
    @patch('pybuilder_anybadge.task.get_vulnerabilities_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_vulnerabilities_badge_Should_CallExpected_When_UseShields(self, update_readme_patch, get_line_to_add_patch, *patches):
        logger_mock = Mock()
        create_vulnerabilities_badge('--report-filename--', '--badge-filename--', logger_mock, use_shields=True)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)

    @patch('pybuilder_anybadge.task.accessible', return_value=False)
    def test__create_coverage_badge_Should_CallExpected_When_NotAccessible(self, *patches):
        logger_mock = Mock()
        create_coverage_badge('--report-filename--', '--badge-filename--', logger_mock)
        logger_mock.warn.assert_called()

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.read_data')
    @patch('pybuilder_anybadge.task.get_coverage')
    @patch('pybuilder_anybadge.task.get_coverage_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_coverage_badge_Should_CallExpected_When_AccessibleCoverage(self, update_readme_patch, get_line_to_add_patch, *patches):
        logger_mock = Mock()
        create_coverage_badge('--report-filename--', '--badge-filename--', logger_mock)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)

    @patch('pybuilder_anybadge.task.accessible', return_value=True)
    @patch('pybuilder_anybadge.task.read_data')
    @patch('pybuilder_anybadge.task.get_coverage')
    @patch('pybuilder_anybadge.task.get_coverage_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_coverage_badge_Should_CallExpected_When_UseShields(self, update_readme_patch, get_line_to_add_patch, *patches):
        logger_mock = Mock()
        create_coverage_badge('--report-filename--', '--badge-filename--', logger_mock, use_shields=True)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)

    @patch('pybuilder_anybadge.task.get_python_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_python_badge_Should_CallExpexted_When_Called(self, update_readme_patch, get_line_to_add_patch, *patches):
        logger_mock = Mock()
        create_python_badge(Mock(), '--badge-filename--', logger_mock)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)

    @patch('pybuilder_anybadge.task.get_python_badge')
    @patch('pybuilder_anybadge.task.get_line_to_add')
    @patch('pybuilder_anybadge.task.update_readme')
    def test__create_python_badge_Should_CallExpexted_When_UseShields(self, update_readme_patch, get_line_to_add_patch, get_python_badge_patch, *patches):
        logger_mock = Mock()
        create_python_badge(Mock(), '--badge--', logger_mock, use_shields=True)
        update_readme_patch.assert_called_once_with(get_line_to_add_patch.return_value, logger_mock)
        get_line_to_add_patch.assert_called_once_with('python', get_python_badge_patch.return_value, True)

    def test__get_python_version_Should_ReturnExpected_When_DistutilsClassifiersContainsPythonVersions(self, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = [
            'Development Status :: 4 - Beta',
            'Environment :: Other Environment',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Topic :: Software Development :: Build Tools'
        ]
        result = get_python_version(project_mock)
        expected_result = '3.7 | 3.8 | 3.9 | 3.10'
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.sys')
    def test__get_python_version_Should_ReturnExpected_When_DistutilsClassifiersDoesNotContainPythonVersions(self, sys_patch, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = [
            'Development Status :: 4 - Beta',
            'Environment :: Other Environment',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Topic :: Software Development :: Build Tools'
        ]
        result = get_python_version(project_mock)
        self.assertEqual(result, f'{sys_patch.version_info.major}.{sys_patch.version_info.minor}')

    @patch('pybuilder_anybadge.task.sys')
    def test__get_python_version_Should_ReturnExpected_When_NoDistutilsClassifiers(self, sys_patch, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = None
        result = get_python_version(project_mock)
        self.assertEqual(result, f'{sys_patch.version_info.major}.{sys_patch.version_info.minor}')
