"""Transaction Management Module."""
import contextlib
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from sqlalchemy.orm import Session

from util.errors import DatabaseError

T = TypeVar("T")


@contextlib.contextmanager
def transaction_context(session: Session):
    """Transaction Context Manager.

    Usage:
    with transaction_context(session) as tx:
        # Execute database operations
    """
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise DatabaseError(
            message=f"Transaction execution failed: {str(e)}", details={"error": str(e)}
        )


def transactional(func: Callable[..., T]) -> Callable[..., T]:
    """Transaction Decorator.

    Usage:
    @transactional
    def some_function(session, ...):
        # Execute database operations
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # Find session parameter
        session = None

        # Look for session in positional arguments
        for arg in args:
            if isinstance(arg, Session):
                session = arg
                break

        # Look for session in keyword arguments
        if session is None:
            session = kwargs.get("session")

        if session is None:
            raise ValueError("Session parameter not found, cannot execute transaction")

        with transaction_context(session):
            return func(*args, **kwargs)

    return cast(Callable[..., T], wrapper)
