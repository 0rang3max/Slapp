from slapp.constants import ReleaseType
from slapp.utils import extract_changelogs, get_random_version_name
from slapp.version import parse_version, Version


def test_extract_changelogs():
    test_data = {
        '* changelog': ['changelog'],
        '* changelog\n* changelog': ['changelog', 'changelog'],
        'some text\n* changelog\n* changelog': ['changelog', 'changelog'],
        'some text\n* changelog\n* changelog\nsome text': ['changelog', 'changelog'],
    }
    for message, changelog in test_data.items():
        assert changelog == extract_changelogs(message)


def test_get_random_name():
    random_names_first = ['nice', 'smart', 'pretty']
    random_names_second = ['dog', 'cow', 'cat']
    random_name = get_random_version_name([random_names_first, random_names_second])
    assert random_name.split(' ')[0] in random_names_first
    assert random_name.split(' ')[1] in random_names_second


def test_parse_version():
    assert parse_version('invalid') is None
    assert parse_version('v1.2.3') is None
    assert parse_version('1.2') is None
    assert parse_version('23') is None

    assert parse_version('0.1.2') == Version(0, 1, 2)
    assert parse_version('1.56.6') == Version(1, 56, 6)
    assert parse_version('4.0.123') == Version(4, 0, 123)


def test_version_compare():
    assert Version(1, 1, 1) == Version(1, 1, 1)

    assert Version(0, 0, 1) < Version(0, 0, 2)
    assert Version(0, 2, 1) < Version(0, 2, 10)
    assert Version(1, 5, 1) < Version(2, 0, 0)

    assert Version(0, 0, 5) > Version(0, 0, 2)
    assert Version(0, 1, 1) > Version(0, 0, 20)
    assert Version(1, 0, 0) > Version(0, 5, 43)
    assert Version(1, 2, 0) > Version(1, 1, 15)


def test_version_default():
    assert Version.get_default() == Version(0, 1, 0)


def test_version_increment():
    assert Version(1, 1, 1).increment(ReleaseType.MAJOR) == Version(2, 0, 0)
    assert Version(1, 1, 1).increment(ReleaseType.MINOR) == Version(1, 2, 0)
    assert Version(1, 1, 1).increment(ReleaseType.PATCH) == Version(1, 1, 2)
