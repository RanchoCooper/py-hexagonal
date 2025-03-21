"""事件处理器实现"""
import logging
from typing import Dict, Any

from application.event.bus import subscribe
from application.event.events import (
    UserCreatedEvent, UserUpdatedEvent, UserDeletedEvent,
    TaskCreatedEvent, TaskUpdatedEvent, TaskCompletedEvent, TaskDeletedEvent,
    Event
)

# 设置日志
logger = logging.getLogger(__name__)


@subscribe("user.created")
def handle_user_created(event: UserCreatedEvent) -> None:
    """处理用户创建事件"""
    logger.info(f"用户已创建: {event.username} (ID: {event.user_id})")
    # 在这里可以添加业务逻辑，例如发送欢迎邮件等


@subscribe("user.updated")
def handle_user_updated(event: UserUpdatedEvent) -> None:
    """处理用户更新事件"""
    logger.info(f"用户已更新: ID {event.user_id}, 更新内容: {event.changes}")
    # 根据更新内容执行相应操作


@subscribe("user.deleted")
def handle_user_deleted(event: UserDeletedEvent) -> None:
    """处理用户删除事件"""
    logger.info(f"用户已删除: ID {event.user_id}")
    # 执行清理操作


@subscribe("task.created")
def handle_task_created(event: TaskCreatedEvent) -> None:
    """处理任务创建事件"""
    user_info = f"(用户: {event.user_id})" if event.user_id else ""
    logger.info(f"任务已创建: '{event.title}' {user_info}")
    # 可以执行其他业务逻辑


@subscribe("task.updated")
def handle_task_updated(event: TaskUpdatedEvent) -> None:
    """处理任务更新事件"""
    user_info = f"(用户: {event.user_id})" if event.user_id else ""
    logger.info(f"任务已更新: ID {event.task_id} {user_info}, 更新内容: {event.changes}")
    # 根据更新内容执行相应操作


@subscribe("task.completed")
def handle_task_completed(event: TaskCompletedEvent) -> None:
    """处理任务完成事件"""
    user_info = f"(用户: {event.user_id})" if event.user_id else ""
    logger.info(f"任务已完成: ID {event.task_id} {user_info}")
    # 可以执行任务完成后的业务逻辑，如通知等


@subscribe("task.deleted")
def handle_task_deleted(event: TaskDeletedEvent) -> None:
    """处理任务删除事件"""
    user_info = f"(用户: {event.user_id})" if event.user_id else ""
    logger.info(f"任务已删除: ID {event.task_id} {user_info}")
    # 执行清理操作


# 通用事件记录器
@subscribe("user.created")
@subscribe("user.updated")
@subscribe("user.deleted")
@subscribe("task.created")
@subscribe("task.updated")
@subscribe("task.completed")
@subscribe("task.deleted")
def log_all_events(event: Event) -> None:
    """记录所有事件到事件日志"""
    logger.debug(f"事件日志: {event.event_type} - {event.to_dict()}")
    # 这里可以将事件持久化到数据库或其他存储 