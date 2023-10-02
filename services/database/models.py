from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "User"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    ...


class Coin(Base):
    __tablename__ = "Coin"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    asset_lable = Column(String(8), nullable=False, unique=True)
    ...


class MultiChequeSubscribes(Base):
    __tablename__ = "MultiChequeSubscribes"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    ...


class MultiChequeBannedLanguages(Base):
    __tablename__ = "MultiChequeBannedLanguages"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    ...


class MultiChequeBannedCountries(Base):
    __tablename__ = "MultiChequeBannedCountries"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    ...


class MultiChequeShare(Base):
    __tablename__ = "MultiChequeShare"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    ...


class MultiCheque(Base):
    __tablename__ = "MultiCheque"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)

    issuer_id = Column(BigInteger, ForeignKey("User.id"))
    amount = Column(BigInteger, default=0, nullable=False)
    currency_id = Column(BigInteger, ForeignKey("Coin.id"))
    activates_count = Column(Integer, default=1, nullable=False)
    referal_reward = Column(BigInteger, default=1)  # [0, 1]

    locked_amount = Column(BigInteger, nullable=False)

    is_pro = Column(Boolean, nullable=False, default=False)
    picture_id = Column(String, nullable=True, default=None)
    description = Column(String, nullable=False, default="")
    password = Column(String, nullable=False, default="")
    is_for_new_users = Column(Boolean, nullable=False, default=False)
    is_require_subscribe = Column(Boolean, default=False, nullable=False)
    is_premium = Column(Boolean, default=False, nullable=False)
    expires_date = Column(DateTime, nullable=True, default=None)
    is_active = Column(Boolean, default=True, nullable=False)
    created_date = Column(DateTime, default=func.now())

    coin = relationship(Coin, foreign_keys=[currency_id], lazy="joined")

    activates = relationship(
        "MultiChequeActivates",
        back_populates="multi_cheque",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )
    subscribes = relationship(
        "MultiChequeSubscribes",
        back_populates="multi_cheque",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )
    banned_languages = relationship(
        "MultiChequeBannedLanguages",
        back_populates="cheque",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )
    countries = relationship(
        "MultiChequeBannedCountries",
        back_populates="multi_cheque",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )
    shared = relationship("MultiChequeShare", lazy="joined")


class MultiChequeActivates(Base):
    __tablename__ = "MultiChequeActivates"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)

    cheque_id = Column(BigInteger, ForeignKey("MultiCheque.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("User.id"), nullable=False)
    reward_amount = Column(BigInteger, nullable=False)
    multi_cheque = relationship("MultiCheque", back_populates="activates")
    visitor_id = Column(String, default="", nullable=False)
    user = relationship("User", back_populates="activations")
