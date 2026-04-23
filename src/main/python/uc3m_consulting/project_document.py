"""Project document entity."""
from datetime import datetime, timezone
import hashlib


class ProjectDocument:
    """Class representing a registered project document."""

    def __init__(self, project_id: str, file_name: str):
        self.__alg = "SHA-256"
        self.__typ = "DOCUMENT"
        self.__project_id = project_id
        self.__file_name = file_name
        justnow = datetime.now(timezone.utc)
        self.__register_date = datetime.timestamp(justnow)

    def __signature_string(self):
        """Build the string used to generate the SHA-256 signature."""
        return (
            "{alg:" + self.__alg +
            ", typ:" + self.__typ +
            ", project_id:" + self.__project_id +
            ", file_name:" + self.__file_name + "}"
        )

    def to_json(self):
        """Return the object data in JSON format."""
        return {
            "alg": self.__alg,
            "typ": self.__typ,
            "project_id": self.__project_id,
            "file_name": self.__file_name,
            "register_date": self.__register_date,
            "file_signature": self.file_signature
        }

    @property
    def project_id(self):
        """Return the project id."""
        return self.__project_id

    @project_id.setter
    def project_id(self, value):
        self.__project_id = value

    @property
    def file_name(self):
        """Return the file name."""
        return self.__file_name

    @file_name.setter
    def file_name(self, value):
        self.__file_name = value

    @property
    def register_date(self):
        """Return the register date."""
        return self.__register_date

    @register_date.setter
    def register_date(self, value):
        self.__register_date = value

    @property
    def file_signature(self):
        """Return the SHA-256 signature."""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()