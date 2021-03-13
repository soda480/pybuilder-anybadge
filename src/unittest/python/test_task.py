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
from pybuilder_anybadge.task import get_severity_badge
from pybuilder_anybadge.task import get_coverage
from pybuilder_anybadge.task import get_coverage_badge
from pybuilder_anybadge.task import update_readme
from pybuilder_anybadge.task import create_complexity_badge
from pybuilder_anybadge.task import create_severity_badge
from pybuilder_anybadge.task import create_coverage_badge


class TestTask(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    def test__init_anybadge_Should_CallExpected_When_Called(self, *patches):
        project_mock = Mock()
        init_anybadge(project_mock)
        self.assertTrue(call('anybadge_exclude', []) in project_mock.set_property_if_unset.mock_calls)
        self.assertTrue(call('anybadge_add_to_readme', False) in project_mock.set_property_if_unset.mock_calls)

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_severity_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeComplexity(self, get_badge_exclude_patch, create_complexity_badge_patch, create_severity_badge_patch, create_coverage_badge_patch, get_images_directory_patch, *patches):
        get_badge_exclude_patch.return_value = ['complexity']
        project_mock = Mock()
        logger_mock = Mock()
        anybadge(project_mock, logger_mock)
        create_complexity_badge_patch.assert_not_called()
        create_severity_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/bandit.json', f'{get_images_directory_patch.return_value}/severity.svg', logger_mock, project_mock.get_property.return_value)
        create_coverage_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/coverage', f'{get_images_directory_patch.return_value}/coverage.svg', logger_mock, project_mock.get_property.return_value)

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_severity_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeSeverity(self, get_badge_exclude_patch, create_complexity_badge_patch, create_severity_badge_patch, create_coverage_badge_patch, get_images_directory_patch, *patches):
        get_badge_exclude_patch.return_value = ['severity']
        project_mock = Mock()
        logger_mock = Mock()
        anybadge(project_mock, logger_mock)
        create_complexity_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/radon', f'{get_images_directory_patch.return_value}/complexity.svg', logger_mock, project_mock.get_property.return_value)
        create_severity_badge_patch.assert_not_called()
        create_coverage_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/coverage', f'{get_images_directory_patch.return_value}/coverage.svg', logger_mock, project_mock.get_property.return_value)

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_severity_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeCoverage(self, get_badge_exclude_patch, create_complexity_badge_patch, create_severity_badge_patch, create_coverage_badge_patch, get_images_directory_patch, *patches):
        get_badge_exclude_patch.return_value = ['coverage']
        project_mock = Mock()
        logger_mock = Mock()
        anybadge(project_mock, logger_mock)
        create_complexity_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/radon', f'{get_images_directory_patch.return_value}/complexity.svg', logger_mock, project_mock.get_property.return_value)
        create_severity_badge_patch.assert_called_once_with(f'{project_mock.expand_path.return_value}/bandit.json', f'{get_images_directory_patch.return_value}/severity.svg', logger_mock, project_mock.get_property.return_value)
        create_coverage_badge_patch.assert_not_called()

    @patch('pybuilder_anybadge.task.get_images_directory')
    @patch('pybuilder_anybadge.task.create_coverage_badge')
    @patch('pybuilder_anybadge.task.create_severity_badge')
    @patch('pybuilder_anybadge.task.create_complexity_badge')
    @patch('pybuilder_anybadge.task.get_badge_exclude')
    def test__anybadge_Should_CallExpected_When_ExcludeAll(self, get_badge_exclude_patch, create_complexity_badge_patch, create_severity_badge_patch, create_coverage_badge_patch, get_images_directory_patch, *patches):
        get_badge_exclude_patch.return_value = ['coverage', 'severity', 'complexity']
        project_mock = Mock()
        logger_mock = Mock()
        anybadge(project_mock, logger_mock)
        create_complexity_badge_patch.assert_not_called()
        create_severity_badge_patch.assert_not_called()
        create_coverage_badge_patch.assert_not_called()

    @patch('pybuilder_anybadge.task.os.path.exists', return_value=False)
    @patch('pybuilder_anybadge.task.os.makedirs')
    def test__get_images_directory_Should_CallAndReturnExpected_When_ImagesDirectoryDoesNotExist(self, makedirs_patch, *patches):
        project_mock = Mock()
        project_mock.expand_path.return_value = '/pybuilder_anybadge/target'
        result = get_images_directory(project_mock)
        expected_result = '/pybuilder_anybadge/docs/images'
        makedirs_patch.assert_called_once_with(expected_result)
        self.assertEqual(result, expected_result)

    @patch('pybuilder_anybadge.task.os.path.exists', return_value=True)
    @patch('pybuilder_anybadge.task.os.makedirs')
    def test__get_images_directory_Should_CallAndReturnExpected_When_ImagesDirectoryDoesExist(self, makedirs_patch, *patches):
        project_mock = Mock()
        project_mock.expand_path.return_value = '/pybuilder_anybadge/target'
        result = get_images_directory(project_mock)
        expected_result = '/pybuilder_anybadge/docs/images'
        makedirs_patch.assert_not_called()
        self.assertEqual(result, expected_result)

    def test__get_badge_exclude_Should_ReturnExpected_When_Exclude(self, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = 'item1,item2'
        result = get_badge_exclude(project_mock)
        expected_result = ['item1', 'item2']
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

    @unittest.skip('skip')
    @patch('builtins.open')
    def test__read_lines_Should_ReturnExpected_When_Called(self, open_patch, *patches):
        open_patch.return_value.__enter__.return_value = mock_open(read_data='line1')
        read_lines('--filename--')

    @patch('builtins.open')
    @patch('pybuilder_anybadge.task.json')
    def test__read_data_Should_ReturnExpected_When_Called(self, json_patch, open_patch, *patches):
        open_patch.return_value.__enter__.return_value = mock_open()
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
            'average': 3.557377049180328,
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
        badge_patch.assert_called_once_with('complexity', value='Simple', default_color='green', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_StableGreen(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 10
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Stable', default_color='green', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_SlightYellow(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 20
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Slight', default_color='yellow', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_ComplexOrange(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 30
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Complex', default_color='orange', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_AlarmingRed(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 40
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Alarming', default_color='red', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_complexity_badge_Should_ReturnExpected_When_UnstableBrightred(self, badge_patch, *patches):
        complexity_report = {
            'highest': {
                'score': 50
            }
        }
        result = get_complexity_badge(complexity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('complexity', value='Unstable', default_color='brightred', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_severity_badge_Should_ReturnExpected_When_GrayUndefined(self, badge_patch, *patches):
        severity_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 1.0,
                    'SEVERITY.LOW': 0.0,
                    'SEVERITY.MEDIUM': 0.0,
                    'SEVERITY.HIGH': 0.0,
                }
            }
        }
        result = get_severity_badge(severity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('severity', value='Undefined', default_color='gray', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_severity_badge_Should_ReturnExpected_When_LowYellow(self, badge_patch, *patches):
        severity_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 0.0,
                    'SEVERITY.LOW': 1.0,
                    'SEVERITY.MEDIUM': 0.0,
                    'SEVERITY.HIGH': 0.0,
                }
            }
        }
        result = get_severity_badge(severity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('severity', value='Low', default_color='yellow', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_severity_badge_Should_ReturnExpected_When_MediumOrange(self, badge_patch, *patches):
        severity_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 0.0,
                    'SEVERITY.LOW': 0.0,
                    'SEVERITY.MEDIUM': 1.0,
                    'SEVERITY.HIGH': 0.0,
                }
            }
        }
        result = get_severity_badge(severity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('severity', value='Medium', default_color='orange', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_severity_badge_Should_ReturnExpected_When_HighRed(self, badge_patch, *patches):
        severity_report = {
            'metrics': {
                '_totals': {
                    'SEVERITY.UNDEFINED': 1.0,
                    'SEVERITY.LOW': 1.0,
                    'SEVERITY.MEDIUM': 1.0,
                    'SEVERITY.HIGH': 1.0,
                }
            }
        }
        result = get_severity_badge(severity_report)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('severity', value='High', default_color='red', num_padding_chars=1)

    def test__get_coverage_Should_Return_Expected_When_Match(self, *patches):
        coverage_lines = [
            'pybuilder_anybadge/task.py         166     64     64      1    60%\n',
            '------------------------------------------------------------------\n',
            'TOTAL                              167     64     64      4    61%\n'
        ]
        result = get_coverage(coverage_lines)
        expected_result = 61
        self.assertEqual(result, expected_result)

    def test__get_coverage_Should_Return_Mpme_When_NoMatch(self, *patches):
        coverage_lines = [
            'pybuilder_anybadge/task.py         166     64     64      1    60%\n',
            '------------------------------------------------------------------\n'
        ]
        result = get_coverage(coverage_lines)
        self.assertIsNone(result)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Green(self, badge_patch, *patches):
        result = get_coverage_badge(100)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='100%', default_color='green', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Yellow(self, badge_patch, *patches):
        result = get_coverage_badge(84)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='84%', default_color='yellow', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Orange(self, badge_patch, *patches):
        result = get_coverage_badge(69)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='69%', default_color='orange', num_padding_chars=1)

    @patch('pybuilder_anybadge.task.Badge')
    def test__get_coverage_badge_Should_ReturnExpected_When_Red(self, badge_patch, *patches):
        result = get_coverage_badge(54)
        self.assertEqual(result, badge_patch.return_value)
        badge_patch.assert_called_once_with('coverage', value='54%', default_color='red', num_padding_chars=1)
