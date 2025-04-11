import logging
import random
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
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

logger = logging.getLogger("BaseQAAgent")

class BaseQAAgent(BaseAgent):
    """
    Base class for all QA agents in the organization.
    Provides common functionality for quality assurance tasks.
    """
    
    def __init__(self, name: str, department: str):
        """
        Initialize the base QA agent with name and department.
        
        Args:
            name: The name of the QA agent
            department: The department the QA agent belongs to
        """
        if not name or not department:
            raise ValueError("Name and department are required")
            
        super().__init__(name, department, "QA")
        self.logger = logging.getLogger(f"{department}.QA.{name}")
        self.logger.info(f"Initializing {name} QA agent in {department} department")
        
        # QA-specific attributes
        self.qa_metrics = {
            "tasks_reviewed": 0,
            "tasks_approved": 0,
            "tasks_rejected": 0,
            "average_review_time": 0.0,
            "quality_score": 0.0
        }
        self.qa_guidelines = {}
        self.qa_checklist = {}
        self.review_history = []
        self.max_review_history = 1000  # Limit review history size
        
    def add_qa_guideline(self, category: str, guideline: str):
        """
        Add a QA guideline for a specific category.
        
        Args:
            category: The category of the guideline
            guideline: The guideline text
        """
        if not category:
            raise ValueError("Category is required")
        if not guideline:
            raise ValueError("Guideline text is required")
            
        if category not in self.qa_guidelines:
            self.qa_guidelines[category] = []
        self.qa_guidelines[category].append(guideline)
        self.logger.info(f"Added QA guideline for {category}: {guideline}")
        
    def add_qa_checklist_item(self, category: str, item: str):
        """
        Add a checklist item for QA review.
        
        Args:
            category: The category of the checklist item
            item: The checklist item text
        """
        if not category:
            raise ValueError("Category is required")
        if not item:
            raise ValueError("Checklist item text is required")
            
        if category not in self.qa_checklist:
            self.qa_checklist[category] = []
        self.qa_checklist[category].append(item)
        self.logger.info(f"Added QA checklist item for {category}: {item}")
        
    def review_task(self, task_id: str, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review a completed task for quality assurance.
        
        Args:
            task_id: The ID of the task to review
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing the review results
        """
        if not task_id:
            raise ValueError("Task ID is required")
        if not isinstance(task_data, dict):
            raise ValueError("Task data must be a dictionary")
        if not isinstance(result, dict):
            raise ValueError("Result must be a dictionary")
            
        self.logger.info(f"Starting QA review for task {task_id}")
        start_time = time.time()
        
        try:
            # Initialize review results
            review_results = {
                "task_id": task_id,
                "reviewer": self.name,
                "timestamp": datetime.now().isoformat(),
                "status": "pending",
                "issues": [],
                "suggestions": [],
                "score": 0.0,
                "decision": None,
                "comments": ""
            }
            
            # Perform checklist review
            checklist_results = self._perform_checklist_review(task_data, result)
            review_results["issues"].extend(checklist_results["issues"])
            review_results["suggestions"].extend(checklist_results["suggestions"])
            
            # Calculate quality score
            review_results["score"] = self._calculate_quality_score(
                checklist_results,
                task_data,
                result
            )
            
            # Validate quality score
            if not 0 <= review_results["score"] <= 1:
                raise ValueError("Quality score must be between 0 and 1")
            
            # Make decision based on quality score
            if review_results["score"] >= 0.8:
                review_results["status"] = "approved"
                review_results["decision"] = "approve"
                self.qa_metrics["tasks_approved"] += 1
            else:
                review_results["status"] = "rejected"
                review_results["decision"] = "reject"
                self.qa_metrics["tasks_rejected"] += 1
                
            # Update metrics
            self.qa_metrics["tasks_reviewed"] += 1
            review_time = time.time() - start_time
            self.qa_metrics["average_review_time"] = (
                (self.qa_metrics["average_review_time"] * (self.qa_metrics["tasks_reviewed"] - 1) + review_time) /
                self.qa_metrics["tasks_reviewed"]
            )
            
            # Add to review history with size limit
            self.review_history.append(review_results)
            if len(self.review_history) > self.max_review_history:
                self.review_history = self.review_history[-self.max_review_history:]
            
            self.logger.info(f"Completed QA review for task {task_id}: {review_results['decision']}")
            return review_results
            
        except Exception as e:
            self.logger.error(f"Error during QA review of task {task_id}: {e}")
            raise
        
    def _perform_checklist_review(self, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a checklist-based review of the task.
        
        Args:
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing issues and suggestions
        """
        review = {
            "issues": [],
            "suggestions": []
        }
        
        # Review each category in the checklist
        for category, items in self.qa_checklist.items():
            for item in items:
                try:
                    # This will be overridden by specific QA agent implementations
                    item_result = self._check_checklist_item(category, item, task_data, result)
                    if item_result["passed"]:
                        continue
                        
                    if item_result["severity"] == "high":
                        review["issues"].append({
                            "category": category,
                            "item": item,
                            "description": item_result["description"]
                        })
                    else:
                        review["suggestions"].append({
                            "category": category,
                            "item": item,
                            "description": item_result["description"]
                        })
                except Exception as e:
                    self.logger.error(f"Error checking checklist item {item} in category {category}: {e}")
                    continue
        
        return review
    
    def _check_checklist_item(self, category: str, item: str, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a specific checklist item.
        
        Args:
            category: The category of the checklist item
            item: The checklist item to check
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing the check results
        """
        # This will be overridden by specific QA agent implementations
        return {
            "passed": True,
            "severity": "low",
            "description": "Default check passed"
        }
    
    def _calculate_quality_score(self, checklist_results: Dict[str, Any], task_data: Dict[str, Any], result: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the task.
        
        Args:
            checklist_results: Results from the checklist review
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        # This will be overridden by specific QA agent implementations
        return 1.0
    
    def get_qa_metrics(self) -> Dict[str, Any]:
        """
        Get the QA agent's performance metrics.
        
        Returns:
            Dictionary containing QA metrics
        """
        return {
            "agent": self.name,
            "department": self.department,
            "metrics": self.qa_metrics,
            "guidelines_count": sum(len(guidelines) for guidelines in self.qa_guidelines.values()),
            "checklist_items_count": sum(len(items) for items in self.qa_checklist.values()),
            "recent_reviews": self.review_history[-10:] if self.review_history else []
        }
    
    def update_qa_guidelines(self, category: str, guidelines: List[str]):
        """
        Update QA guidelines for a category.
        
        Args:
            category: The category to update
            guidelines: List of new guidelines
        """
        if not category:
            raise ValueError("Category is required")
        if not isinstance(guidelines, list):
            raise ValueError("Guidelines must be a list")
            
        self.qa_guidelines[category] = guidelines
        self.logger.info(f"Updated QA guidelines for {category}")
        
    def update_qa_checklist(self, category: str, items: List[str]):
        """
        Update QA checklist for a category.
        
        Args:
            category: The category to update
            items: List of new checklist items
        """
        if not category:
            raise ValueError("Category is required")
        if not isinstance(items, list):
            raise ValueError("Items must be a list")
            
        self.qa_checklist[category] = items
        self.logger.info(f"Updated QA checklist for {category}")
        
    def clear_review_history(self):
        """
        Clear the review history.
        """
        self.review_history = []
        self.logger.info("Cleared review history")
        
    def __str__(self) -> str:
        """
        String representation of the QA agent.
        
        Returns:
            String describing the QA agent
        """
        return f"{self.name} (QA) - {self.department} Department" 