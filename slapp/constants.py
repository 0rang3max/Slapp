from enum import Enum

CONFIG_FILE = 'slapp.yml'

DEFAULT_CONFIG = {
    'repo_directory': '.git',
    'release_branch': 'main',
    'changelog_file': 'CHANGELOG.md',
    'bullet': '*',
}


class ReleaseType(Enum):
    MAJOR = 'major'
    MINOR = 'minor'
    PATCH = 'patch'

    def __str__(self):
        return self.value

    @classmethod
    def get_values(cls):
        return list(map(str, cls))
