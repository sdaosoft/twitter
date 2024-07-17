from pathlib import Path
from typing import Sequence, Iterable

from pydantic import Field
import pyotp

from .utils import hidden_value, load_lines, write_lines
from .enums import AccountStatus
from .models import User


class Account(User):
    # fmt: off
    auth_token:  str | None = Field(default=None, pattern=r"^[a-f0-9]{40}$")
    ct0:         str | None = None  # 160
    password:    str | None = None  # 128
    email:       str | None = None  # 254
    email_password:       str | None = None  # 254
    totp_secret: str | None = None  # 16
    backup_code: str | None = None  # 12
    status: AccountStatus = AccountStatus.UNKNOWN
    # fmt: on

    @property
    def hidden_auth_token(self) -> str | None:
        return hidden_value(self.auth_token) if self.auth_token else None

    @property
    def hidden_password(self) -> str | None:
        return hidden_value(self.password) if self.password else None

    @property
    def hidden_totp_secret(self) -> str | None:
        return hidden_value(self.totp_secret) if self.totp_secret else None

    @property
    def hidden_backup_code(self) -> str | None:
        return hidden_value(self.backup_code) if self.backup_code else None

    def __str__(self):
        return self.hidden_auth_token

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username}, auth_token={self.hidden_auth_token})"

    def update(self, **data: dict):
        update = self.dict()
        update.update(data)
        for k, v in self.validate(update).dict(exclude_defaults=True).items():
            setattr(self, k, v)

    def get_totp_code(self) -> str | None:
        if not self.totp_secret:
            raise ValueError("No totp_secret")

        return str(pyotp.TOTP(self.totp_secret).now())
