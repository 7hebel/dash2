"""
Module: version.py
Check online version, handle versions.
"""
import requests


class Version:
    """ Represents version. """

    def __init__(self, major: int, minor: int, patch: int) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch
        
        self.as_text: str = str(self)
        self.as_tuple: tuple[int, int, int] = (self.major, self.minor, self.patch)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __gt__(self, other_version: "Version") -> bool:
        if self.as_tuple == other_version.as_tuple: return False
        return Version.__a_greater_than_b(self, other_version)

    def __lt__(self, other_version: "Version") -> bool:
        if self.as_tuple == other_version.as_tuple: return False
        return not Version.__a_greater_than_b(self, other_version)

    def __eq__(self, other_version: "Version") -> bool:
        return self.as_tuple == other_version.as_tuple

    @staticmethod
    def __a_greater_than_b(a: "Version", b: "Version") -> bool:
        """ Check if version a is greater than version b. """

        for a_value, b_value in zip([a.major, a.minor, a.patch], 
                                    [b.major, b.minor, b.patch]):
            if a_value > b_value: return True
            if a_value < b_value: return False

def get_version_from_text(text: str) -> "Version":
    """ Return Version object from text in format: "major.minor.patch" """
    parts = text.strip().split(".")

    major = int(parts[0])
    minor = int(parts[1])
    patch = int(parts[2])

    return Version(major, minor, patch)

def get_online_version() -> Version:
    """ Get newest available version. """
    url = "https://raw.githubusercontent.com/gental-py/dash2/main/.update"
    try:
        response = requests.get(url, timeout=3).json()["version"]
        version = get_version_from_text(response)
    except:
        version = Version(0,0,0)

    return version
