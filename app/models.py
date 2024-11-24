from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
# The db instance is from Flask-SQLAlchemy
from app import db

# The class inherits from db.Model, a base class for all models from Flask-SQLAlchemy.
class User(db.Model):
    # Fields are assigned a type using Python type hints, wrapped with SQLAlchemy's so.Mapped generic type.
    # A type declaration such as so.Mapped[int] or so.Mapped[str] define the type of the column, and also make values required, or non-nullable in database terms.
    # To define a column that is allowed to be empty or nullable, the Optional helper from Python is also added, as password_hash demonstrates.
    # In most cases defining a table column requires more than the column type.
    # SQLAlchemy uses a so.mapped_column() function call assigned to each column to provide this additional configuration.
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    # This is not an actual database field, but a high-level view of the relationship between users and posts.
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    # The __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
