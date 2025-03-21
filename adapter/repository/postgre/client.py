"""
PostgreSQL client module.
"""

import sys
from contextlib import contextmanager
from typing import Any, Dict, Iterator, List, Optional

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from adapter.repository.error import PersistenceError
from domain.repo.transaction import Transaction


class PostgreSQLError(PersistenceError):
    """Error raised when there's a problem with PostgreSQL."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(f"PostgreSQL error: {message}", cause)


class PostgreSQLClient:
    """PostgreSQL client wrapper."""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        password: str = "",
        database: str = "",
        schema: str = "public",
        pool_size: int = 5,
        pool_recycle: int = 3600,
    ):
        """
        Initialize the PostgreSQL client.
        
        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            user: PostgreSQL user
            password: PostgreSQL password
            database: PostgreSQL database name
            schema: PostgreSQL schema
            pool_size: Connection pool size
            pool_recycle: Connection pool recycle time in seconds
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema
        self.pool_size = pool_size
        self.pool_recycle = pool_recycle
        self._engine: Optional[Engine] = None
        self._session_factory = None
    
    def connect(self) -> None:
        """
        Connect to the PostgreSQL database.
        
        Raises:
            PostgreSQLError: If the connection fails
        """
        try:
            connection_str = (
                f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            )
            self._engine = create_engine(
                connection_str,
                pool_size=self.pool_size,
                pool_recycle=self.pool_recycle,
                pool_pre_ping=True,
                future=True,
                connect_args={"options": f"-c search_path={self.schema}"}
            )
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                future=True,
            )
        except Exception as e:
            raise PostgreSQLError(f"Failed to connect to PostgreSQL: {e}", e)
    
    @contextmanager
    def session(self) -> Iterator[Session]:
        """
        Get a new session.
        
        Yields:
            A new SQLAlchemy session
            
        Raises:
            PostgreSQLError: If the session creation fails
        """
        if self._engine is None:
            self.connect()
            
        if self._session_factory is None:
            raise PostgreSQLError("PostgreSQL client is not connected")
            
        session = self._session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise PostgreSQLError(f"PostgreSQL session error: {e}", e)
        finally:
            session.close()


class PostgreSQLTransaction(Transaction):
    """PostgreSQL transaction implementation."""
    
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
            PostgreSQLError: If the commit fails
        """
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise PostgreSQLError(f"Failed to commit transaction: {e}", e)
    
    def rollback(self) -> None:
        """
        Rollback the transaction.
        
        Raises:
            PostgreSQLError: If the rollback fails
        """
        try:
            self.session.rollback()
        except Exception as e:
            raise PostgreSQLError(f"Failed to rollback transaction: {e}", e) 