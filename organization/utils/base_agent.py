import os
import json
import logging
import random
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import requests
from datetime import datetime
import asyncio

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

logger = logging.getLogger("BaseAgent")

class BaseAgent(ABC):
    """
    Base class for all agents in the organization.
    Provides common functionality and interface for all agents.
    """
    
    def __init__(self, name: str, department: str, role: str):
        """
        Initialize the base agent with name, department, and role.
        
        Args:
            name: The name of the agent
            department: The department the agent belongs to
            role: The role of the agent
        """
        if not name or not department or not role:
            raise ValueError("Name, department, and role are required")
            
        self.name = name
        self.department = department
        self.role = role
        self.logger = logging.getLogger(f"{department}.{name}")
        self.logger.info(f"Initializing {name} agent in {department} department as {role}")
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 0.0,
            "average_processing_time": 0.0,
            "last_task_time": None
        }
        self.task_history = []
        self.is_busy = False
        self.current_task = None
        self.skills = self._initialize_skills()
        self.knowledge_base = self._initialize_knowledge_base()
        
    def _initialize_skills(self) -> Dict[str, float]:
        """
        Initialize the agent's skills with proficiency levels.
        
        Returns:
            Dictionary of skills and their proficiency levels (0.0 to 1.0)
        """
        # This will be overridden by specific agent implementations
        return {}
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """
        Initialize the agent's knowledge base.
        
        Returns:
            Dictionary containing the agent's knowledge
        """
        # This will be overridden by specific agent implementations
        return {}
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and return the results.
        This method must be implemented by all agent subclasses.
        
        Args:
            input_data: Dictionary containing input data for processing
            
        Returns:
            Dictionary containing the results of processing
        """
        pass
    
    def update_metrics(self, success: bool, processing_time: float):
        """
        Update the agent's performance metrics.
        
        Args:
            success: Whether the task was successful
            processing_time: Time taken to process the task in seconds
        """
        if processing_time < 0:
            raise ValueError("Processing time cannot be negative")
            
        self.performance_metrics["tasks_completed"] += 1
        
        # Update success rate
        current_success_rate = self.performance_metrics["success_rate"]
        total_tasks = self.performance_metrics["tasks_completed"]
        self.performance_metrics["success_rate"] = (
            (current_success_rate * (total_tasks - 1) + (1.0 if success else 0.0)) / total_tasks
        )
        
        # Update average processing time
        current_avg_time = self.performance_metrics["average_processing_time"]
        self.performance_metrics["average_processing_time"] = (
            (current_avg_time * (total_tasks - 1) + processing_time) / total_tasks
        )
        
        self.performance_metrics["last_task_time"] = datetime.now().isoformat()
        
        self.logger.info(f"Updated metrics: {self.performance_metrics}")
    
    def log_task(self, task_id: str, input_data: Dict[str, Any], output_data: Dict[str, Any], 
                 success: bool, processing_time: float):
        """
        Log a completed task.
        
        Args:
            task_id: Unique identifier for the task
            input_data: Input data for the task
            output_data: Output data from the task
            success: Whether the task was successful
            processing_time: Time taken to process the task in seconds
        """
        if not task_id:
            raise ValueError("Task ID is required")
            
        task_log = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "output": output_data,
            "success": success,
            "processing_time": processing_time
        }
        
        self.task_history.append(task_log)
        self.logger.info(f"Task {task_id} completed with success={success}, time={processing_time}s")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """
        Generate a performance report for the agent.
        
        Returns:
            Dictionary containing performance metrics
        """
        return {
            "name": self.name,
            "department": self.department,
            "role": self.role,
            "metrics": self.performance_metrics,
            "recent_tasks": self.task_history[-5:] if self.task_history else []
        }
    
    def is_available(self) -> bool:
        """
        Check if the agent is available to take on a new task.
        
        Returns:
            True if the agent is available, False otherwise
        """
        return not self.is_busy
    
    def assign_task(self, task_id: str, task_data: Dict[str, Any]) -> bool:
        """
        Assign a task to the agent.
        
        Args:
            task_id: Unique identifier for the task
            task_data: Data for the task
            
        Returns:
            True if the task was assigned successfully, False otherwise
        """
        if not task_id:
            raise ValueError("Task ID is required")
            
        if self.is_busy:
            self.logger.warning(f"Cannot assign task {task_id} to busy agent {self.name}")
            return False
        
        self.is_busy = True
        self.current_task = {
            "task_id": task_id,
            "data": task_data,
            "start_time": datetime.now().isoformat()
        }
        self.logger.info(f"Assigned task {task_id} to agent {self.name}")
        return True
    
    def complete_task(self, task_id: str, result: Dict[str, Any], success: bool = True):
        """
        Mark a task as completed.
        
        Args:
            task_id: Unique identifier for the task
            result: Result of the task
            success: Whether the task was successful
        """
        if not task_id:
            raise ValueError("Task ID is required")
            
        if not self.current_task or self.current_task["task_id"] != task_id:
            self.logger.error(f"Cannot complete task {task_id} - not assigned to agent {self.name}")
            return
        
        try:
            start_time = datetime.fromisoformat(self.current_task["start_time"])
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            self.log_task(task_id, self.current_task["data"], result, success, processing_time)
            self.update_metrics(success, processing_time)
            
            self.is_busy = False
            self.current_task = None
            self.logger.info(f"Completed task {task_id}")
        except Exception as e:
            self.logger.error(f"Error completing task {task_id}: {e}")
            raise
    
    def simulate_thinking(self, min_time: float = 0.5, max_time: float = 2.0):
        """
        Simulate the agent thinking about a task.
        This is used to make the agent behavior more realistic.
        
        Args:
            min_time: Minimum thinking time in seconds
            max_time: Maximum thinking time in seconds
        """
        if min_time < 0 or max_time < 0 or min_time > max_time:
            raise ValueError("Invalid thinking time parameters")
            
        thinking_time = random.uniform(min_time, max_time)
        time.sleep(thinking_time)
    
    def get_skill_proficiency(self, skill: str) -> float:
        """
        Get the agent's proficiency in a specific skill.
        
        Args:
            skill: The skill to check
            
        Returns:
            Proficiency level (0.0 to 1.0)
        """
        if not skill:
            raise ValueError("Skill name is required")
        return self.skills.get(skill, 0.0)
    
    def improve_skill(self, skill: str, improvement: float = 0.1):
        """
        Improve the agent's proficiency in a specific skill.
        
        Args:
            skill: The skill to improve
            improvement: Amount to improve by (0.0 to 1.0)
        """
        if not skill:
            raise ValueError("Skill name is required")
        if not 0 <= improvement <= 1:
            raise ValueError("Improvement must be between 0 and 1")
            
        if skill in self.skills:
            current_proficiency = self.skills[skill]
            self.skills[skill] = min(1.0, current_proficiency + improvement)
            self.logger.info(f"Improved {skill} skill from {current_proficiency:.2f} to {self.skills[skill]:.2f}")
        else:
            self.skills[skill] = min(1.0, improvement)
            self.logger.info(f"Added new skill {skill} with proficiency {self.skills[skill]:.2f}")
    
    def add_to_knowledge_base(self, key: str, value: Any):
        """
        Add information to the agent's knowledge base.
        
        Args:
            key: Key for the knowledge
            value: Value to store
        """
        if not key:
            raise ValueError("Knowledge key is required")
        self.knowledge_base[key] = value
        self.logger.info(f"Added knowledge: {key}")
    
    def get_from_knowledge_base(self, key: str) -> Optional[Any]:
        """
        Retrieve information from the agent's knowledge base.
        
        Args:
            key: Key for the knowledge
            
        Returns:
            The value if found, None otherwise
        """
        if not key:
            raise ValueError("Knowledge key is required")
        return self.knowledge_base.get(key)
    
    def make_decision(self, options: List[Tuple[str, float]]) -> str:
        """
        Make a decision based on weighted options.
        
        Args:
            options: List of tuples containing (option, weight)
            
        Returns:
            The selected option
        """
        if not options:
            raise ValueError("Options list cannot be empty")
            
        total_weight = sum(weight for _, weight in options)
        if total_weight <= 0:
            return options[0][0] if options else ""
        
        normalized_options = [(option, weight / total_weight) for option, weight in options]
        r = random.random()
        cumulative_weight = 0
        
        for option, weight in normalized_options:
            cumulative_weight += weight
            if r <= cumulative_weight:
                return option
        
        return normalized_options[-1][0]
    
    def __str__(self) -> str:
        """
        String representation of the agent.
        
        Returns:
            String describing the agent
        """
        return f"{self.name} ({self.role}) - {self.department} Department" 