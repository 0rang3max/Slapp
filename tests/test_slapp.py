from slapp.utils import (
    extract_changelogs, increment_version
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
