from slapp.utils import (
    extract_changelogs, increment_version, get_random_version_name
)


def test_extract_changelogs():
    test_data = {
        '* changelog': ['changelog'],
        '* changelog\n* changelog': ['changelog', 'changelog'],
        'some text\n* changelog\n* changelog': ['changelog', 'changelog'],
        'some text\n* changelog\n* changelog\nsome text': ['changelog', 'changelog'],
    }
    for message, changelog in test_data.items():
        assert changelog == extract_changelogs(message)


def test_autoincrement():
    assert increment_version('1.1.1', 'patch') == '1.1.2'
    assert increment_version('1.1.1', 'minor') == '1.2.0'
    assert increment_version('1.1.1', 'major') == '2.0.0'


def test_get_random_name():
    random_names_first = ['nice', 'smart', 'pretty']
    random_names_second = ['dog', 'cow', 'cat']
    random_name = get_random_version_name([random_names_first, random_names_second])
    assert random_name.split(' ')[0] in random_names_first
    assert random_name.split(' ')[1] in random_names_second
