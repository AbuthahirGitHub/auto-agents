import asyncio
import logging
from organization.utils.base_agent import BaseAgent
from organization.utils.base_manager import BaseManager
from organization.utils.base_qa_agent import BaseQAAgent
from organization.departments.marketing.agents.marketing_agent import MarketingAgent
from organization.departments.marketing.managers.marketing_manager import MarketingManager
from organization.departments.marketing.qa.marketing_qa_agent import MarketingQAAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_organization")

async def test_marketing_agent():
    """Test the MarketingAgent class"""
    logger.info("Testing MarketingAgent...")
    try:
        agent = MarketingAgent("TestAgent")
        logger.info(f"Created agent: {agent}")
        
        # Test process method
        result = await agent.process({
            "type": "content_creation",
            "topic": "Test Topic",
            "target_audience": ["Test Audience"],
            "channel": "Test Channel"
        })
        logger.info(f"Process result: {result}")
        
        # Test get_marketing_metrics
        metrics = agent.get_marketing_metrics()
        logger.info(f"Marketing metrics: {metrics}")
        
        logger.info("MarketingAgent test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error testing MarketingAgent: {e}")
        return False

async def test_marketing_manager():
    """Test the MarketingManager class"""
    logger.info("Testing MarketingManager...")
    try:
        manager = MarketingManager("TestManager")
        logger.info(f"Created manager: {manager}")
        
        # Test process_department_task method
        result = await manager.process_department_task({
            "type": "strategy_development",
            "name": "Test Strategy",
            "goals": ["Test Goal"],
            "target_audiences": ["Test Audience"],
            "channels": ["Test Channel"]
        })
        logger.info(f"Process department task result: {result}")
        
        # Test get_marketing_metrics
        metrics = manager.get_marketing_metrics()
        logger.info(f"Marketing metrics: {metrics}")
        
        logger.info("MarketingManager test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error testing MarketingManager: {e}")
        return False

async def test_marketing_qa_agent():
    """Test the MarketingQAAgent class"""
    logger.info("Testing MarketingQAAgent...")
    try:
        qa_agent = MarketingQAAgent("TestQAAgent")
        logger.info(f"Created QA agent: {qa_agent}")
        
        # Test process method
        task_data = {
            "type": "content_creation",
            "topic": "Test Topic",
            "target_audience": ["Test Audience"],
            "channel": "Test Channel"
        }
        
        result = {
            "content": {
                "id": "content_123",
                "type": "content_creation",
                "topic": "Test Topic",
                "target_audience": ["Test Audience"],
                "channel": "Test Channel",
                "format": "blog",
                "tone": "professional",
                "keywords": ["test", "marketing"],
                "call_to_action": "Learn more",
                "created_at": "2025-04-12T04:24:19.487825"
            }
        }
        
        review_result = await qa_agent.process({
            "task_data": task_data,
            "result": result
        })
        logger.info(f"Process result: {review_result}")
        
        logger.info("MarketingQAAgent test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error testing MarketingQAAgent: {e}")
        return False

async def main():
    """Run all tests"""
    logger.info("Starting organization tests...")
    
    # Test base classes
    logger.info("Testing base classes...")
    try:
        # These will raise NotImplementedError since they're abstract
        # We just want to make sure they can be instantiated
        BaseAgent("TestBaseAgent", "Test", "Test")
        BaseManager("TestBaseManager", "Test")
        BaseQAAgent("TestBaseQAAgent", "Test")
        logger.info("Base classes test completed successfully")
    except NotImplementedError:
        # This is expected since the process methods are abstract
        logger.info("Base classes test completed as expected")
    except Exception as e:
        logger.error(f"Error testing base classes: {e}")
    
    # Test marketing implementations
    agent_success = await test_marketing_agent()
    manager_success = await test_marketing_manager()
    qa_agent_success = await test_marketing_qa_agent()
    
    if agent_success and manager_success and qa_agent_success:
        logger.info("All tests completed successfully!")
    else:
        logger.error("Some tests failed!")

if __name__ == "__main__":
    asyncio.run(main()) 