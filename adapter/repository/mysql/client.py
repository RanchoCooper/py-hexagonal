"""
MySQL client module.
"""

import sys
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from adapter.repository.error import MySQLError
from domain.repo.transaction import Transaction


class MySQLClient:
    """MySQL client wrapper."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: str = "",
        charset: str = "utf8mb4",
        pool_size: int = 5,
        pool_recycle: int = 3600,
    ):
        """
        Initialize the MySQL client.
        
        Args:
            host: MySQL host
            port: MySQL port
            user: MySQL user
            password: MySQL password
            database: MySQL database name
            charset: MySQL charset
            pool_size: Connection pool size
            pool_recycle: Connection pool recycle time in seconds
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.pool_size = pool_size
        self.pool_recycle = pool_recycle
        self._engine: Optional[Engine] = None
        self._session_factory = None
    
    def connect(self) -> None:
        """
        Connect to the MySQL database.
        
        Raises:
            MySQLError: If the connection fails
        """
        try:
            connection_str = (
                f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
                f"?charset={self.charset}"
            )
            self._engine = create_engine(
                connection_str,
                pool_size=self.pool_size,
                pool_recycle=self.pool_recycle,
                pool_pre_ping=True,
                future=True,
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                future=True,
            )
        except Exception as e:
            raise MySQLError(f"Failed to connect to MySQL: {e}", e)
    
    @contextmanager
    def session(self) -> Iterator[Session]:
        """
        Get a new session.
        
        Yields:
            A new SQLAlchemy session
            
        Raises:
            MySQLError: If the session creation fails
        """
        if self._engine is None:
            self.connect()
            
        if self._session_factory is None:
            raise MySQLError("MySQL client is not connected")
            
        session = self._session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise MySQLError(f"MySQL session error: {e}", e)
        finally:
            session.close()


class MySQLTransaction(Transaction):
    """MySQL transaction implementation."""
    
    def __init__(self, session: Session):
        """
        Initialize the transaction.
        
        Args:
            session: The SQLAlchemy session
        """
        self.session = session
    
    def commit(self) -> None:
        """
        Commit the transaction.
        
        Raises:
            MySQLError: If the commit fails
        """
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise MySQLError(f"Failed to commit transaction: {e}", e)
    
    def rollback(self) -> None:
        """
        Rollback the transaction.
        
        Raises:
            MySQLError: If the rollback fails
        """
        try:
            self.session.rollback()
        except Exception as e:
            raise MySQLError(f"Failed to rollback transaction: {e}", e) 