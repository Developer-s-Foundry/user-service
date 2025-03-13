from pydantic import BaseModel

from src.api.enums.Currency import Currency


class AddWithdrawalAccountRequest(BaseModel):
    user: str
    bank_name: str
    bank_code: str
    account_number: str
    account_name: str
    currency: Currency
