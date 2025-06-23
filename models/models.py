from typing import Any, List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, REAL, Table, Text, text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        PrimaryKeyConstraint('event_type', name='event_pkey'),
    )

    event_type: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text)

    logged: Mapped[List['Logged']] = relationship('Logged', back_populates='event')


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = (
        PrimaryKeyConstraint('id_tag', name='tag_pkey'),
    )

    id_tag: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag_content: Mapped[str] = mapped_column(Text)
    color: Mapped[int] = mapped_column(Integer)

    generaluser: Mapped[List['Generaluser']] = relationship('Generaluser', back_populates='tag')


class Generaluser(Base):
    __tablename__ = 'generaluser'
    __table_args__ = (
        ForeignKeyConstraint(['id_tag'], ['tag.id_tag'], name='generaluser_id_tag_fkey'),
        PrimaryKeyConstraint('id_user', name='generaluser_pkey')
    )

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    permission_level: Mapped[int] = mapped_column(Integer)
    fake_username: Mapped[Optional[str]] = mapped_column(Text)
    id_tag: Mapped[Optional[int]] = mapped_column(Integer)

    tag: Mapped[Optional['Tag']] = relationship('Tag', back_populates='generaluser')
    generaluser: Mapped[List['Generaluser']] = relationship('Generaluser', secondary='following', primaryjoin=lambda: Generaluser.id_user == t_following.c.follower, secondaryjoin=lambda: Generaluser.id_user == t_following.c.following, back_populates='generaluser_')
    generaluser_: Mapped[List['Generaluser']] = relationship('Generaluser', secondary='following', primaryjoin=lambda: Generaluser.id_user == t_following.c.following, secondaryjoin=lambda: Generaluser.id_user == t_following.c.follower, back_populates='generaluser')
    logged: Mapped[List['Logged']] = relationship('Logged', back_populates='generaluser')
    post: Mapped[List['Post']] = relationship('Post', back_populates='generaluser')
    reacted_to: Mapped[List['ReactedTo']] = relationship('ReactedTo', back_populates='generaluser')


class Ai(Generaluser):
    __tablename__ = 'ai'
    __table_args__ = (
        ForeignKeyConstraint(['id_user'], ['generaluser.id_user'], name='ai_id_user_fkey'),
        PrimaryKeyConstraint('id_user', name='ai_pkey')
    )

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_name: Mapped[str] = mapped_column(Text)
    prompt: Mapped[str] = mapped_column(Text)
    max_comment_length: Mapped[Optional[int]] = mapped_column(Integer)
    comments_context_size: Mapped[Optional[int]] = mapped_column(Integer)
    temp: Mapped[Optional[float]] = mapped_column(REAL)
    min_p: Mapped[Optional[float]] = mapped_column(REAL)


class Aiverified(Base):
    __tablename__ = 'aiverified'
    __table_args__ = (
        ForeignKeyConstraint(['id_user'], ['generaluser.id_user'], name='aiverified_id_user_fkey'),
        PrimaryKeyConstraint('id_user', name='aiverified_pkey')
    )

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    last_profile_change: Mapped[datetime.datetime] = mapped_column(DateTime)
    last_post_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('to_timestamp((0)::double precision)'))
    last_ai_verification: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('to_timestamp((0)::double precision)'))


t_following = Table(
    'following', Base.metadata,
    Column('following', Integer, primary_key=True, nullable=False),
    Column('follower', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['follower'], ['generaluser.id_user'], name='following_follower_fkey'),
    ForeignKeyConstraint(['following'], ['generaluser.id_user'], name='following_following_fkey'),
    PrimaryKeyConstraint('following', 'follower', name='following_pkey')
)


class Logged(Base):
    __tablename__ = 'logged'
    __table_args__ = (
        ForeignKeyConstraint(['event_type'], ['event.event_type'], name='logged_event_type_fkey'),
        ForeignKeyConstraint(['id_user'], ['generaluser.id_user'], name='logged_id_user_fkey'),
        PrimaryKeyConstraint('id_logged', name='logged_pkey')
    )

    id_logged: Mapped[int] = mapped_column(Integer, primary_key=True)
    time: Mapped[datetime.datetime] = mapped_column(DateTime)
    ipv4: Mapped[Any] = mapped_column(INET)
    id_user: Mapped[int] = mapped_column(Integer)
    event_type: Mapped[int] = mapped_column(Integer)
    page: Mapped[Optional[str]] = mapped_column(Text)

    event: Mapped['Event'] = relationship('Event', back_populates='logged')
    generaluser: Mapped['Generaluser'] = relationship('Generaluser', back_populates='logged')


class Post(Base):
    __tablename__ = 'post'
    __table_args__ = (
        ForeignKeyConstraint(['id_user'], ['generaluser.id_user'], name='post_id_user_fkey'),
        PrimaryKeyConstraint('id_post', name='post_pkey')
    )

    id_post: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_: Mapped[str] = mapped_column('text', Text)
    time: Mapped[datetime.datetime] = mapped_column(DateTime)
    like_count: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    is_reply: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    is_trending: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))
    id_user: Mapped[Optional[int]] = mapped_column(Integer)

    generaluser: Mapped[Optional['Generaluser']] = relationship('Generaluser', back_populates='post')
    reacted_to: Mapped[List['ReactedTo']] = relationship('ReactedTo', back_populates='post')


class ReactedTo(Base):
    __tablename__ = 'reacted_to'
    __table_args__ = (
        ForeignKeyConstraint(['id_post'], ['post.id_post'], name='reacted_to_id_post_fkey'),
        ForeignKeyConstraint(['id_user'], ['generaluser.id_user'], name='reacted_to_id_user_fkey'),
        PrimaryKeyConstraint('id_user', 'id_post', name='reacted_to_pkey')
    )

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_post: Mapped[int] = mapped_column(Integer, primary_key=True)
    liked: Mapped[bool] = mapped_column(Boolean, server_default=text('false'))

    post: Mapped['Post'] = relationship('Post', back_populates='reacted_to')
    generaluser: Mapped['Generaluser'] = relationship('Generaluser', back_populates='reacted_to')
