# buskill imports
from buskill.utils.config.objects.types import TypedConfig, EncodedTypedConfig

# datetime imports
from datetime import date

# typing imports
from typing import TypedDict

class Identity(TypedConfig):
    first_name: str
    family_name: str
    date_of_birth: date | None

class Contact(TypedConfig):
    emails: set[str]
    phone_numbers: set[str]
    social_medias: dict[str, set[str]]

class RecoveryConfig(TypedConfig):
    identity: Identity
    contact: Contact
    message: str
    enabled: bool

class EncodedDate(TypedDict):
    day: int
    month: int
    year: int

class EncodedIdentity(EncodedTypedConfig):
    first_name: str
    family_name: str
    date_of_birth: EncodedDate | None

class EncodedContact(EncodedTypedConfig):
    emails: list[str]
    phone_numbers: list[str]
    social_medias: dict[str, list[str]]

class EncodedRecoveryConfig(EncodedTypedConfig):
    identity: EncodedIdentity
    contact: EncodedContact
    message: str
    enabled: bool