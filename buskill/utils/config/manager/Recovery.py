# typing imports
from typing import Self, Literal, Iterable

# buskill imports
from buskill.utils.config.objects import RecoveryConfig, Identity, Contact, EncodedIdentity, EncodedContact, EncodedRecoveryConfig, EncodedDate
from buskill.utils.config.manager import Manager, ApplyFunc

# datetime imports
from datetime import date

# re imports
import re

class IdentityManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: Identity
        self._apply: ApplyFunc = apply

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'identity')
        self._apply(param_path)

    def load_config(self: Self, config: Identity) -> None:
        self._config = config
        self.apply([])

    def change_first_name(self: Self, first_name: str) -> None:
        self._config['first_name'] = first_name
        self.apply(['first_name'])

    def change_family_name(self: Self, family_name: str) -> None:
        self._config['family_name'] = family_name
        self.apply(['family_name'])

    def change_date_of_birth(self: Self, date_of_birth: date) -> None:
        self._config['date_of_birth'] = date_of_birth
        self.apply(['date_of_birth'])

    @property
    def first_name(self: Self) -> str:
        return self._config['first_name']

    @property
    def family_name(self: Self) -> str:
        return self._config['family_name']

    @property
    def date_of_birth(self: Self) -> date | None:
        return self._config['date_of_birth']

    @property
    def get(self: Self) -> Identity:
        return self._config

    @property
    def encoded(self: Self) -> EncodedIdentity:
        encoded_date_of_birth: EncodedDate | None
        if self.date_of_birth is None: 
            encoded_date_of_birth = None
        else: 
            encoded_date_of_birth = {
                'day': self.date_of_birth.day,
                'month': self.date_of_birth.month,
                'year': self.date_of_birth.year
            }

        return {
            'first_name': self.first_name,
            'family_name': self.family_name,
            'date_of_birth': encoded_date_of_birth
        }

    def decode(self: Self, encoded_config: EncodedIdentity) -> Identity:
        date_of_birth: date | None
        if encoded_config['date_of_birth'] is None:
            date_of_birth = None
        else:
            try:
                date_of_birth = date(
                    encoded_config['date_of_birth']['year'],
                    encoded_config['date_of_birth']['month'],
                    encoded_config['date_of_birth']['day']
                )
            except:
                date_of_birth = None

        return {
            'first_name': encoded_config['first_name'],
            'family_name': encoded_config['family_name'],
            'date_of_birth': date_of_birth
        }

class ContactManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: Contact
        self._apply: ApplyFunc = apply

        # We type as Literal so if someone accidently modify a LOC, there will be an error visible instantly (incoherence between the type and the value)
        self._email_pattern: Literal["^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"]
        self._email_pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

        self._phone_number_pattern: Literal['^(?:\\+[0-9]{1,3}[ -]?[0-9]|0[0-9])(?:[ -]?[0-9]{2})*$']
        self._phone_number_pattern = r'^(?:\+[0-9]{1,3}[ -]?[0-9]|0[0-9])(?:[ -]?[0-9]{2})*$'

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'contact')
        self._apply(param_path)

    def load_config(self: Self, config: Contact) -> None:
        self._config = config
        self.apply([])

    def add_emails(self: Self, emails: set[str]) -> None:
        for email in emails:
            if re.match(self._email_pattern, email) is not None:
                self._config['emails'].add(email)
        self.apply(['emails'])

    def clear_emails(self: Self) -> None:
        self._config['emails'].clear()
        self.apply(['emails'])

    def add_phone_numbers(self: Self, phone_numbers: set[str]) -> None:
        for phone_number in phone_numbers:
            if re.match(self._phone_number_pattern, phone_number) is not None:
                self._config['phone_numbers'].add(phone_number)
        self.apply(['phone_numbers'])

    def clear_phone_numbers(self: Self) -> None:
        self._config['phone_numbers'].clear()
        self.apply(['phone_numbers'])

    def add_social_medias(self: Self, social_medias: dict[str, set[str]]) -> None:
        for social_media in social_medias.keys():
            if self._config['social_medias'].get(social_media) is None:
                self._config['social_medias'][social_media] = social_medias[social_media]
            else:
                self._config['social_medias'][social_media] |= social_medias[social_media]
        self.apply(['social_medias'])

    def remove_social_medias(self: Self, social_medias: dict[str, set[str]]) -> None:
        for social_media in social_medias.keys():
            if self._config['social_medias'].get(social_media):
                if '@all' in social_medias[social_media]:
                    del self._config['social_medias'][social_media]
                else:
                    self._config['social_medias'][social_media] -= social_medias[social_media]
                    if len(self._config['social_medias'][social_media]) == 0:
                        del self._config['social_medias'][social_media]
        self.apply(['social_medias'])

    def clear_social_medias(self: Self) -> None:
        self._config['social_medias'].clear()
        self.apply(['social_medias'])

    @property
    def emails(self: Self) -> set[str]:
        return self._config['emails']

    @property
    def phone_numbers(self: Self) -> set[str]:
        return self._config['phone_numbers']

    @property
    def social_medias(self: Self) -> dict[str, set[str]]:
        return self._config['social_medias']

    @property
    def list_social_medias(self: Self) -> Iterable[str]:
        return self._config['social_medias'].keys()

    @property
    def get(self: Self) -> Contact:
        return self._config

    @property
    def _encoded_social_medias(self: Self) -> dict[str, list[str]]:
        encoded_social_medias: dict[str, list[str]] = {}
        for social_media in self.list_social_medias:
            encoded_social_medias[social_media] = sorted(list(self.social_medias[social_media]))
        return encoded_social_medias

    def _decode_social_medias(self: Self, encoded_social_medias: dict[str, list[str]]) -> dict[str, set[str]]:
        social_medias: dict[str, set[str]] = {}
        for social_media in encoded_social_medias:
            social_medias[social_media] = set(encoded_social_medias[social_media])
        return social_medias

    @property
    def encoded(self: Self) -> EncodedContact:
        return {
            'emails': sorted(list(self.emails)),
            'phone_numbers': sorted(list(self.phone_numbers)),
            'social_medias': self._encoded_social_medias
        }

    def decode(self: Self, encoded_config: EncodedContact) -> Contact:
        return {
            'emails': set(encoded_config['emails']),
            'phone_numbers': set(encoded_config['phone_numbers']),
            'social_medias': self._decode_social_medias(encoded_config['social_medias'])
        }
        
class RecoveryManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: RecoveryConfig
        self._apply: ApplyFunc = apply

        self.identity: IdentityManager = IdentityManager(self.apply)
        self.contact: ContactManager = ContactManager(self.apply)

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'recovery')
        self._apply(param_path)

    def load_config(self: Self, config: RecoveryConfig) -> None:
        self._config = config
        self.identity.load_config(self._config['identity'])
        self.contact.load_config(self._config['contact'])

    def change_message(self: Self, message: str) -> None:
        self._config['message'] = message

    def replace_identity(self: Self, identity: Identity) -> None:
        self._config['identity'] = identity
        self.identity.load_config(self._config['identity'])

    def replace_contact(self: Self, contact: Contact) ->  None:
        self._config['contact'] = contact
        self.contact.load_config(self._config['contact'])

    @property
    def message(self: Self) -> str:
        return self._config['message']

    @property
    def get(self: Self) -> RecoveryConfig:
        return self._config

    @property
    def encoded(self: Self) -> EncodedRecoveryConfig:
        return {
            'identity': self.identity.encoded,
            'contact': self.contact.encoded,
            'message': self.message
        }

    def decode(self: Self, encoded_config: EncodedRecoveryConfig) -> RecoveryConfig:
        return {
            'identity': self.identity.decode(encoded_config['identity']),
            'contact': self.contact.decode(encoded_config['contact']),
            'message': encoded_config['message']
        }