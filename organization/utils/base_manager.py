import logging
import random
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from .base_agent import BaseAgent

# Configure logging with error handling
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("organization.log"),
            logging.StreamHandler()
        ]
    )
except Exception as e:
    print(f"Failed to configure logging: {e}")
    # Fallback to basic console logging
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("BaseManager")

class BaseManager(ABC):
    """
    Base class for all managers in the organization.
    Provides common functionality for managing teams of agents.
    """
    
    def __init__(self, name: str, department: str):
        """
        Initialize the base manager with name and department.
        
        Args:
            name: The name of the manager
            department: The department the manager belongs to
        """
        if not name or not department:
            raise ValueError("Name and department are required")
            
        self.name = name
        self.department = department
        self.logger = logging.getLogger(f"{department}.Manager.{name}")
        self.logger.info(f"Initializing {name} manager in {department} department")
        
        self.agents = {}  # Dictionary of agent_id -> agent
        self.qa_agents = {}  # Dictionary of qa_agent_id -> qa_agent
        self.tasks = {}  # Dictionary of task_id -> task
        self.task_queue = []  # List of task_ids in order of priority
        self.performance_metrics = {
            "tasks_assigned": 0,
            "tasks_completed": 0,
            "average_completion_time": 0.0,
            "team_efficiency": 0.0
        }
        self.team_knowledge_base = {}
        self.team_skills = {}
        
    def add_agent(self, agent: BaseAgent) -> str:
        """
        Add an agent to the manager's team.
        
        Args:
            agent: The agent to add
            
        Returns:
            The agent's ID
        """
        if not isinstance(agent, BaseAgent):
            raise ValueError("Agent must be an instance of BaseAgent")
            
        agent_id = str(uuid.uuid4())
        self.agents[agent_id] = agent
        self.logger.info(f"Added agent {agent.name} to team with ID {agent_id}")
        return agent_id
    
    def add_qa_agent(self, qa_agent: BaseAgent) -> str:
        """
        Add a QA agent to the manager's team.
        
        Args:
            qa_agent: The QA agent to add
            
        Returns:
            The QA agent's ID
        """
        if not isinstance(qa_agent, BaseAgent):
            raise ValueError("QA agent must be an instance of BaseAgent")
            
        qa_agent_id = str(uuid.uuid4())
        self.qa_agents[qa_agent_id] = qa_agent
        self.logger.info(f"Added QA agent {qa_agent.name} to team with ID {qa_agent_id}")
        return qa_agent_id
    
    def remove_agent(self, agent_id: str) -> bool:
        """
        Remove an agent from the manager's team.
        
        Args:
            agent_id: The ID of the agent to remove
            
        Returns:
            True if the agent was removed, False otherwise
        """
        if not agent_id:
            raise ValueError("Agent ID is required")
            
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            self.logger.info(f"Removed agent {agent.name} from team")
            return True
        return False
    
    def remove_qa_agent(self, qa_agent_id: str) -> bool:
        """
        Remove a QA agent from the manager's team.
        
        Args:
            qa_agent_id: The ID of the QA agent to remove
            
        Returns:
            True if the QA agent was removed, False otherwise
        """
        if not qa_agent_id:
            raise ValueError("QA agent ID is required")
            
        if qa_agent_id in self.qa_agents:
            qa_agent = self.qa_agents.pop(qa_agent_id)
            self.logger.info(f"Removed QA agent {qa_agent.name} from team")
            return True
        return False
    
    def create_task(self, task_type: str, task_data: Dict[str, Any], priority: int = 1) -> str:
        """
        Create a new task and add it to the task queue.
        
        Args:
            task_type: The type of task
            task_data: Data for the task
            priority: Priority of the task (higher number = higher priority)
            
        Returns:
            The task ID
        """
        if not task_type:
            raise ValueError("Task type is required")
        if not isinstance(task_data, dict):
            raise ValueError("Task data must be a dictionary")
        if not isinstance(priority, int) or priority < 1:
            raise ValueError("Priority must be a positive integer")
            
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "type": task_type,
            "data": task_data,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "assigned_to": None,
            "completed_at": None,
            "result": None,
            "qa_status": "pending",
            "qa_result": None
        }
        
        self.tasks[task_id] = task
        
        # Add to queue based on priority
        inserted = False
        for i, queued_task_id in enumerate(self.task_queue):
            if self.tasks[queued_task_id]["priority"] < priority:
                self.task_queue.insert(i, task_id)
                inserted = True
                break
        
        if not inserted:
            self.task_queue.append(task_id)
        
        self.logger.info(f"Created task {task_id} of type {task_type} with priority {priority}")
        return task_id
    
    def assign_tasks(self):
        """
        Assign pending tasks to available agents.
        """
        if not self.task_queue:
            self.logger.info("No tasks to assign")
            return
            
        if not self.agents:
            self.logger.warning("No agents available to assign tasks")
            return
        
        for task_id in self.task_queue:
            task = self.tasks[task_id]
            
            # Skip tasks that are already assigned or completed
            if task["status"] != "pending":
                continue
            
            # Find an available agent with the right skills
            assigned = False
            for agent_id, agent in self.agents.items():
                if agent.is_available() and self._agent_can_handle_task(agent, task):
                    task["status"] = "assigned"
                    task["assigned_to"] = agent_id
                    agent.assign_task(task_id, task["data"])
                    self.logger.info(f"Assigned task {task_id} to agent {agent.name}")
                    assigned = True
                    break
            
            if not assigned:
                self.logger.warning(f"Could not find an available agent for task {task_id}")
    
    def _agent_can_handle_task(self, agent: BaseAgent, task: Dict[str, Any]) -> bool:
        """
        Check if an agent can handle a specific task.
        
        Args:
            agent: The agent to check
            task: The task to check
            
        Returns:
            True if the agent can handle the task, False otherwise
        """
        # This will be overridden by specific manager implementations
        return True
    
    def update_task_status(self, task_id: str, status: str, result: Optional[Dict[str, Any]] = None):
        """
        Update the status of a task.
        
        Args:
            task_id: The ID of the task to update
            status: The new status
            result: The result of the task (if completed)
        """
        if not task_id:
            raise ValueError("Task ID is required")
        if not status:
            raise ValueError("Status is required")
            
        if task_id not in self.tasks:
            self.logger.error(f"Cannot update status of non-existent task {task_id}")
            return
        
        task = self.tasks[task_id]
        task["status"] = status
        
        if status == "completed" and result is not None:
            task["result"] = result
            task["completed_at"] = datetime.now().isoformat()
            
            # Assign to QA if available
            if self.qa_agents:
                qa_agent_id = random.choice(list(self.qa_agents.keys()))
                qa_agent = self.qa_agents[qa_agent_id]
                if qa_agent.is_available():
                    task["qa_status"] = "assigned"
                    qa_agent.assign_task(task_id, {
                        "task_data": task["data"],
                        "result": result
                    })
                    self.logger.info(f"Assigned task {task_id} to QA agent {qa_agent.name}")
        
        self.logger.info(f"Updated task {task_id} status to {status}")
    
    def update_qa_status(self, task_id: str, status: str, result: Optional[Dict[str, Any]] = None):
        """
        Update the QA status of a task.
        
        Args:
            task_id: The ID of the task to update
            status: The new QA status
            result: The QA result
        """
        if not task_id:
            raise ValueError("Task ID is required")
        if not status:
            raise ValueError("Status is required")
            
        if task_id not in self.tasks:
            self.logger.error(f"Cannot update QA status of non-existent task {task_id}")
            return
        
        task = self.tasks[task_id]
        task["qa_status"] = status
        
        if status == "approved" or status == "rejected":
            task["qa_result"] = result
            
            # Update task status based on QA result
            if status == "approved":
                task["status"] = "approved"
            elif status == "rejected":
                task["status"] = "rejected"
                # Put back in queue with higher priority
                if task_id in self.task_queue:
                    self.task_queue.remove(task_id)
                task["priority"] += 1
                self.task_queue.append(task_id)
        
        self.logger.info(f"Updated task {task_id} QA status to {status}")
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a task by ID.
        
        Args:
            task_id: The ID of the task to get
            
        Returns:
            The task if found, None otherwise
        """
        if not task_id:
            raise ValueError("Task ID is required")
        return self.tasks.get(task_id)
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: The ID of the agent to get
            
        Returns:
            The agent if found, None otherwise
        """
        if not agent_id:
            raise ValueError("Agent ID is required")
        return self.agents.get(agent_id)
    
    def get_qa_agent(self, qa_agent_id: str) -> Optional[BaseAgent]:
        """
        Get a QA agent by ID.
        
        Args:
            qa_agent_id: The ID of the QA agent to get
            
        Returns:
            The QA agent if found, None otherwise
        """
        if not qa_agent_id:
            raise ValueError("QA agent ID is required")
        return self.qa_agents.get(qa_agent_id)
    
    def get_team_performance_report(self) -> Dict[str, Any]:
        """
        Generate a performance report for the manager's team.
        
        Returns:
            Dictionary containing team performance metrics
        """
        agent_reports = {
            agent_id: agent.get_performance_report()
            for agent_id, agent in self.agents.items()
        }
        
        qa_reports = {
            qa_agent_id: qa_agent.get_performance_report()
            for qa_agent_id, qa_agent in self.qa_agents.items()
        }
        
        # Calculate team efficiency
        if self.performance_metrics["tasks_completed"] > 0:
            self.performance_metrics["team_efficiency"] = (
                self.performance_metrics["tasks_completed"] / 
                max(1, self.performance_metrics["tasks_assigned"])
            )
        
        return {
            "manager": self.name,
            "department": self.department,
            "metrics": self.performance_metrics,
            "agents": agent_reports,
            "qa_agents": qa_reports,
            "pending_tasks": len([t for t in self.tasks.values() if t["status"] == "pending"]),
            "completed_tasks": len([t for t in self.tasks.values() if t["status"] == "completed"]),
            "approved_tasks": len([t for t in self.tasks.values() if t["status"] == "approved"]),
            "rejected_tasks": len([t for t in self.tasks.values() if t["status"] == "rejected"])
        }
    
    def update_team_knowledge(self, key: str, value: Any):
        """
        Update the team's knowledge base.
        
        Args:
            key: Key for the knowledge
            value: Value to store
        """
        if not key:
            raise ValueError("Knowledge key is required")
            
        self.team_knowledge_base[key] = value
        self.logger.info(f"Updated team knowledge: {key}")
        
        # Share knowledge with all agents
        for agent in self.agents.values():
            agent.add_to_knowledge_base(key, value)
    
    def update_team_skills(self, skill: str, improvement: float = 0.1):
        """
        Update the team's skills.
        
        Args:
            skill: The skill to improve
            improvement: Amount to improve by (0.0 to 1.0)
        """
        if not skill:
            raise ValueError("Skill name is required")
        if not 0 <= improvement <= 1:
            raise ValueError("Improvement must be between 0 and 1")
            
        current_skill = self.team_skills.get(skill, 0.0)
        self.team_skills[skill] = min(1.0, current_skill + improvement)
        self.logger.info(f"Updated team skill {skill} to {self.team_skills[skill]:.2f}")
        
        # Share skill improvement with all agents
        for agent in self.agents.values():
            agent.improve_skill(skill, improvement)
    
    def hold_team_meeting(self, agenda: List[str]) -> Dict[str, Any]:
        """
        Simulate a team meeting to discuss progress and share knowledge.
        
        Args:
            agenda: List of topics to discuss
            
        Returns:
            Dictionary containing meeting outcomes
        """
        if not agenda:
            raise ValueError("Agenda cannot be empty")
            
        self.logger.info(f"Starting team meeting with agenda: {agenda}")
        
        meeting_outcomes = {
            "date": datetime.now().isoformat(),
            "attendees": [agent.name for agent in self.agents.values()] + 
                         [qa_agent.name for qa_agent in self.qa_agents.values()],
            "agenda": agenda,
            "decisions": {},
            "action_items": []
        }
        
        # Simulate meeting discussion
        for topic in agenda:
            self.logger.info(f"Discussing topic: {topic}")
            time.sleep(random.uniform(0.5, 1.5))
            
            # Generate a decision for this topic
            decision = self._generate_meeting_decision(topic)
            meeting_outcomes["decisions"][topic] = decision
            
            # Generate action items
            if random.random() < 0.7:  # 70% chance of having action items
                action_item = {
                    "topic": topic,
                    "action": f"Follow up on {topic}",
                    "assigned_to": random.choice(list(self.agents.keys())),
                    "due_date": (datetime.now() + timedelta(days=random.randint(1, 7))).isoformat()
                }
                meeting_outcomes["action_items"].append(action_item)
        
        self.logger.info("Team meeting completed")
        return meeting_outcomes
    
    def _generate_meeting_decision(self, topic: str) -> str:
        """
        Generate a decision for a meeting topic.
        
        Args:
            topic: The topic to generate a decision for
            
        Returns:
            The decision
        """
        # This will be overridden by specific manager implementations
        return f"Decision regarding {topic}"
    
    @abstractmethod
    async def process_department_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a department-level task.
        This method must be implemented by all manager subclasses.
        
        Args:
            task_data: Dictionary containing task data
            
        Returns:
            Dictionary containing the results of processing
        """
        pass
    
    def cleanup_old_tasks(self, days: int = 30):
        """
        Clean up tasks older than the specified number of days.
        
        Args:
            days: Number of days after which to clean up tasks
        """
        if days < 0:
            raise ValueError("Days must be non-negative")
            
        cutoff_date = datetime.now() - timedelta(days=days)
        tasks_to_remove = []
        
        for task_id, task in self.tasks.items():
            if task["status"] in ["completed", "approved", "rejected"]:
                task_date = datetime.fromisoformat(task["created_at"])
                if task_date < cutoff_date:
                    tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            self.tasks.pop(task_id)
            if task_id in self.task_queue:
                self.task_queue.remove(task_id)
        
        self.logger.info(f"Cleaned up {len(tasks_to_remove)} old tasks")
    
    def __str__(self) -> str:
        """
        String representation of the manager.
        
        Returns:
            String describing the manager
        """
        return f"{self.name} (Manager) - {self.department} Department" 