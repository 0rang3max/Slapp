from slapp.utils import extract_changelogs


def test_extract_changelogs():
    test_data = {
        '* changelog': ['changelog'],
        '* changelog\n* changelog': ['changelog', 'changelog'],
        'some text\n* changelog\n* changelog': ['changelog', 'changelog'],
        'some text\n* changelog\n* changelog\nsome text': ['changelog', 'changelog'],
    }
    for message, changelog in test_data.items():
        assert changelog == extract_changelogs(message)
