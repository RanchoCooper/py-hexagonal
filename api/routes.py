"""API路由定义"""
from flask import Blueprint, request, jsonify, g
from datetime import datetime
import logging

from util.errors import ValidationError, NotFoundError
from application.service.example import (
    CreateUserUseCase, GetUserUseCase, UpdateUserUseCase, DeleteUserUseCase,
    CreateTaskUseCase, GetTaskUseCase, UpdateTaskUseCase, CompleteTaskUseCase,
    DeleteTaskUseCase, ListUserTasksUseCase
)
from application.usecase.example import (
    CreateUserInput, UpdateUserInput, CreateTaskInput, UpdateTaskInput
)
from api.middleware import auth_required

# 设置日志
logger = logging.getLogger(__name__)

# 创建蓝图
api_blueprint = Blueprint('api', __name__)


# 用户相关路由
@api_blueprint.route('/users', methods=['POST'])
def create_user():
    """创建用户"""
    data = request.json
    
    if not data:
        raise ValidationError(message="请求体不能为空")
    
    # 验证必填字段
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            raise ValidationError(message=f"缺少必填字段: {field}")
    
    # 创建用例输入
    input_data = CreateUserInput(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        full_name=data.get('full_name')
    )
    
    # 执行用例
    usecase = CreateUserUseCase()
    result = usecase.execute(input_data)
    
    # 返回结果
    return jsonify({
        'id': result.id,
        'username': result.username,
        'email': result.email,
        'full_name': result.full_name,
        'is_active': result.is_active,
        'created_at': result.created_at.isoformat()
    }), 201


@api_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户"""
    usecase = GetUserUseCase()
    result = usecase.execute(user_id)
    
    return jsonify({
        'id': result.id,
        'username': result.username,
        'email': result.email,
        'full_name': result.full_name,
        'is_active': result.is_active,
        'created_at': result.created_at.isoformat()
    })


@api_blueprint.route('/users/<user_id>', methods=['PUT'])
@auth_required
def update_user(user_id):
    """更新用户"""
    data = request.json
    
    if not data:
        raise ValidationError(message="请求体不能为空")
    
    # 创建用例输入
    input_data = UpdateUserInput(
        user_id=user_id,
        username=data.get('username'),
        email=data.get('email'),
        full_name=data.get('full_name'),
        is_active=data.get('is_active')
    )
    
    # 执行用例
    usecase = UpdateUserUseCase()
    result = usecase.execute(input_data)
    
    # 返回结果
    return jsonify({
        'id': result.id,
        'username': result.username,
        'email': result.email,
        'full_name': result.full_name,
        'is_active': result.is_active,
        'created_at': result.created_at.isoformat()
    })


@api_blueprint.route('/users/<user_id>', methods=['DELETE'])
@auth_required
def delete_user(user_id):
    """删除用户"""
    usecase = DeleteUserUseCase()
    result = usecase.execute(user_id)
    
    return jsonify({'success': result})


# 任务相关路由
@api_blueprint.route('/tasks', methods=['POST'])
@auth_required
def create_task():
    """创建任务"""
    data = request.json
    
    if not data:
        raise ValidationError(message="请求体不能为空")
    
    # 验证必填字段
    if 'title' not in data:
        raise ValidationError(message="缺少必填字段: title")
    
    # 处理日期字段
    due_date = None
    if 'due_date' in data and data['due_date']:
        try:
            due_date = datetime.fromisoformat(data['due_date'])
        except ValueError:
            raise ValidationError(message="日期格式无效，请使用ISO格式 (YYYY-MM-DDTHH:MM:SS)")
    
    # 创建用例输入
    input_data = CreateTaskInput(
        title=data['title'],
        description=data.get('description'),
        due_date=due_date,
        user_id=data.get('user_id', g.get('user_id'))
    )
    
    # 执行用例
    usecase = CreateTaskUseCase()
    result = usecase.execute(input_data)
    
    # 准备响应
    response = {
        'id': result.id,
        'title': result.title,
        'description': result.description,
        'is_completed': result.is_completed,
        'user_id': result.user_id,
        'created_at': result.created_at.isoformat()
    }
    
    if result.due_date:
        response['due_date'] = result.due_date.isoformat()
    
    # 返回结果
    return jsonify(response), 201


@api_blueprint.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """获取任务"""
    usecase = GetTaskUseCase()
    result = usecase.execute(task_id)
    
    # 准备响应
    response = {
        'id': result.id,
        'title': result.title,
        'description': result.description,
        'is_completed': result.is_completed,
        'user_id': result.user_id,
        'created_at': result.created_at.isoformat()
    }
    
    if result.due_date:
        response['due_date'] = result.due_date.isoformat()
    
    return jsonify(response)


@api_blueprint.route('/tasks/<task_id>', methods=['PUT'])
@auth_required
def update_task(task_id):
    """更新任务"""
    data = request.json
    
    if not data:
        raise ValidationError(message="请求体不能为空")
    
    # 处理日期字段
    due_date = None
    if 'due_date' in data:
        if data['due_date'] is None:
            due_date = None
        else:
            try:
                due_date = datetime.fromisoformat(data['due_date'])
            except ValueError:
                raise ValidationError(message="日期格式无效，请使用ISO格式 (YYYY-MM-DDTHH:MM:SS)")
    
    # 创建用例输入
    input_data = UpdateTaskInput(
        task_id=task_id,
        title=data.get('title'),
        description=data.get('description'),
        due_date=due_date
    )
    
    # 执行用例
    usecase = UpdateTaskUseCase()
    result = usecase.execute(input_data)
    
    # 准备响应
    response = {
        'id': result.id,
        'title': result.title,
        'description': result.description,
        'is_completed': result.is_completed,
        'user_id': result.user_id,
        'created_at': result.created_at.isoformat()
    }
    
    if result.due_date:
        response['due_date'] = result.due_date.isoformat()
    
    return jsonify(response)


@api_blueprint.route('/tasks/<task_id>/complete', methods=['POST'])
@auth_required
def complete_task(task_id):
    """完成任务"""
    usecase = CompleteTaskUseCase()
    result = usecase.execute(task_id)
    
    # 准备响应
    response = {
        'id': result.id,
        'title': result.title,
        'description': result.description,
        'is_completed': result.is_completed,
        'user_id': result.user_id,
        'created_at': result.created_at.isoformat()
    }
    
    if result.due_date:
        response['due_date'] = result.due_date.isoformat()
    
    return jsonify(response)


@api_blueprint.route('/tasks/<task_id>', methods=['DELETE'])
@auth_required
def delete_task(task_id):
    """删除任务"""
    usecase = DeleteTaskUseCase()
    result = usecase.execute(task_id)
    
    return jsonify({'success': result})


@api_blueprint.route('/users/<user_id>/tasks', methods=['GET'])
def list_user_tasks(user_id):
    """获取用户的所有任务"""
    usecase = ListUserTasksUseCase()
    results = usecase.execute(user_id)
    
    # 准备响应
    tasks = []
    for result in results:
        task = {
            'id': result.id,
            'title': result.title,
            'description': result.description,
            'is_completed': result.is_completed,
            'user_id': result.user_id,
            'created_at': result.created_at.isoformat()
        }
        
        if result.due_date:
            task['due_date'] = result.due_date.isoformat()
        
        tasks.append(task)
    
    return jsonify(tasks)
