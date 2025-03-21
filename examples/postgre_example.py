"""
PostgreSQL example for the hexagonal architecture project.
"""

import sys
from datetime import datetime
from uuid import uuid4

# Add project root to Python path
sys.path.append(".")

from adapter.repository.postgre.client import PostgreSQLClient
from adapter.repository.postgre.example_repo import PostgreSQLExampleRepository
from adapter.repository.postgre.transaction_manager import PostgreSQLTransactionManager
from domain.model.example import Example


def main():
    """
    Main function for the PostgreSQL example.
    
    This example demonstrates:
    1. Creating a PostgreSQL client
    2. Creating an example repository
    3. Creating an example
    4. Saving the example
    5. Finding the example by ID
    6. Finding the example by name
    7. Updating the example
    8. Finding all examples
    9. Deleting the example
    10. Using transactions
    """
    # Create a PostgreSQL client
    postgresql_client = PostgreSQLClient(
        "postgresql://username:password@localhost:5432/example_db"
    )
    
    # Create an example repository
    example_repo = PostgreSQLExampleRepository(postgresql_client)
    
    # Create a transaction manager
    transaction_manager = PostgreSQLTransactionManager(postgresql_client)
    
    # Create a new example
    example_id = uuid4()
    example = Example(
        id=example_id,
        name="测试示例",
        description="这是一个测试示例",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Using a transaction to save the example
    try:
        def save_example():
            return example_repo.save(example)
            
        saved_example = transaction_manager.with_transaction(save_example)
        print(f"已保存示例: {saved_example.id}, {saved_example.name}")
        
        # Find the example by ID
        found_by_id = example_repo.find_by_id(example_id)
        if found_by_id:
            print(f"通过ID找到示例: {found_by_id.id}, {found_by_id.name}")
        else:
            print("未找到示例")
            
        # Find the example by name
        found_by_name = example_repo.find_by_name("测试示例")
        if found_by_name:
            print(f"通过名称找到示例: {found_by_name.id}, {found_by_name.name}")
        else:
            print("未通过名称找到示例")
            
        # Update the example
        found_by_id.update(
            name="更新后的示例",
            description="这是一个更新后的示例描述"
        )
        updated_example = example_repo.save(found_by_id)
        print(f"已更新示例: {updated_example.id}, {updated_example.name}")
        
        # Find all examples
        all_examples = example_repo.find_all()
        print(f"找到 {len(all_examples)} 个示例:")
        for e in all_examples:
            print(f"  - {e.id}, {e.name}, {'活跃' if e.is_active else '非活跃'}")
            
        # Delete the example
        example_repo.delete(example_id)
        print(f"已删除示例: {example_id}")
        
        # Verify deletion
        deleted_example = example_repo.find_by_id(example_id)
        if deleted_example is None:
            print("确认示例已删除")
        else:
            print("示例未被删除")
    
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main() 