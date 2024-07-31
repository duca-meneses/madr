from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


@table_registry.mapped_as_dataclass
class Novelist:
    __tablename__ = 'novelists'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list['Book']] = relationship(
        init=False, back_populates='novelists', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[str]
    author: Mapped[Novelist] = relationship(init=False, back_populates='books')
