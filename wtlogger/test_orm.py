from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test.db", echo=True)

metadata = MetaData(engine)

Base = declarative_base(metadata=metadata)


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    genre = Column(String(250))

    def __repr__(self):
        return f"<Book(id={self.id} title={self.title} author={self.author} genre={self.genre})>"


Base.metadata.create_all(engine)


Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

session = Session()

# bookOne = Book(title="The me bee", author="Bla", genre="lala")

# session.add(bookOne)
# session.commit()

print(session.query(Book).all())


edited_book = session.query(Book).filter_by(id=1).one()
edited_book.author = "DDD"
session.add(edited_book)
session.commit()

book_delete = session.query(Book).filter_by(author="DDD").one()
session.delete(book_delete)
session.commit()
