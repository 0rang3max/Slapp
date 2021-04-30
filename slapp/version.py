import copy
import re

from slapp.constants import ReleaseType

VALID_TAG_REGEX = r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'


def parse_version(version: str):
    if not re.match(VALID_TAG_REGEX, version):
        return None
    major, minor, patch = [int(i) for i in version.split('.')]
    return Version(major, minor, patch)


class Version:
    DEFAULT_VERSION = '0.1.0'

    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'

    def __repr__(self):
        return f'<Version: {str(self)}>'

    def __eq__(self, other):
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch
        )

    def __gt__(self, other):
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        return self.patch > other.patch

    def __lt__(self, other):
        return self != other and not self > other

    def increment(self, release_type: ReleaseType):
        new_version = copy.deepcopy(self)
        if release_type == ReleaseType.MAJOR:
            new_version.major += 1
            new_version.minor = new_version.patch = 0
        elif release_type == ReleaseType.MINOR:
            new_version.minor += 1
            new_version.patch = 0
        else:
            new_version.patch += 1
        return new_version

    @classmethod
    def get_default(cls):
        return parse_version(cls.DEFAULT_VERSION)
