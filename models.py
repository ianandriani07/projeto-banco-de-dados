from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class GeneralUser(Base):
    __tablename__ = 'generaluser'
    
    id_user = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    description = Column(String, nullable=False)
    permission_level = Column(Integer, nullable=False)
    fake_username = Column(String, nullable=True)

    def __repr__(self):
        return f"<GeneralUser(username={self.username}, email={self.email})>"


"""
CREATE TABLE GeneralUser (
    ID_user integer PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL,
    email text NOT NULL,
    description text NOT NULL,
    permission_level integer NOT NULL,
    fake_username text
"""