from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Coin, MultiCheque, MultiChequeActivates

AnyModel = Coin | MultiCheque | MultiChequeActivates


class DAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_cheque_by_id(self, cheque_id: int) -> Optional[MultiCheque]:
        statement = select(MultiCheque).where(MultiCheque.id == cheque_id)

        result = await self.session.execute(statement)
        return result.scalar()

    def add(self, instance: AnyModel) -> None:
        self.session.add(instance=instance)

    async def commit(self) -> None:
        await self.session.commit()

    async def close(self) -> None:
        await self.session.close()
