from typing import Optional

from pydantic import BaseModel


class MultiChequeStatistics(BaseModel):
    total_requests: int

    bots_blocked: Optional[int]
    multi_accounts_blocked: Optional[int]
    activations: int

    activations_by_country: dict[str, int]
