from enum import Enum

CONFIG_FILE = 'slapp.yml'

DEFAULT_CONFIG = {
    'repo_directory': '.git',
    'release_branch': 'master',
    'changelog_file': 'CHANGELOG.md',
    'bullet': '*',
}


class ReleaseType(Enum):
    MAJOR = 'major'
    MINOR = 'minor'
    PATCH = 'patch'

    def __str__(self):
        return self.value
