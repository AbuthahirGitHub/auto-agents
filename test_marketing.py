import asyncio
from organization.departments.marketing.agents.marketing_agent import MarketingAgent
from organization.departments.marketing.managers.marketing_manager import MarketingManager
from organization.departments.marketing.qa.marketing_qa_agent import MarketingQAAgent

async def test_marketing_components():
    # Create instances
    agent = MarketingAgent("TestAgent")
    manager = MarketingManager("TestManager")
    qa_agent = MarketingQAAgent("TestQA")
    
    # Test agent
    print("\nTesting MarketingAgent...")
    task_data = {
        "type": "content_creation",
        "content_type": "blog_post",
        "topic": "Test Topic",
        "target_audience": ["test_audience"],
        "keywords": ["test", "keywords"]
    }
    result = await agent.process(task_data)
    print(f"Agent process result: {result}")
    
    # Test manager
    print("\nTesting MarketingManager...")
    dept_task = {
        "type": "strategy_development",
        "name": "Test Strategy",
        "goals": ["test_goal"],
        "timeline": {"start_date": "2024-04-01", "end_date": "2024-04-30"},
        "target_audiences": ["test_audience"],
        "channels": ["test_channel"],
        "budget": {"total": 1000},
        "success_metrics": ["test_metric"]
    }
    result = await manager.process_department_task(dept_task)
    print(f"Manager process result: {result}")
    
    # Test QA agent
    print("\nTesting MarketingQAAgent...")
    review_data = {
        "task_id": "test_task",
        "task_type": "content",
        "content": {
            "text": "Test content",
            "tone": "professional",
            "call_to_action": "Test CTA",
            "keywords": ["test"]
        }
    }
    result = await qa_agent.review_task(review_data)
    print(f"QA review result: {result}")

if __name__ == "__main__":
    asyncio.run(test_marketing_components()) 