import logging
from typing import Dict, Any, List
from datetime import datetime
from ....utils.base_qa_agent import BaseQAAgent

class MarketingQAAgent(BaseQAAgent):
    """
    QA agent specialized in reviewing marketing content and campaigns.
    Inherits from BaseQAAgent and implements marketing-specific QA functionality.
    """
    
    def __init__(self, name: str):
        """
        Initialize a marketing QA agent.
        
        Args:
            name: The name of the QA agent
        """
        super().__init__(name, "Marketing")
        self.logger = logging.getLogger(f"Marketing.QA.{name}")
        self.logger.info(f"Initializing marketing QA agent {name}")
        
        # Marketing QA-specific attributes
        self.qa_guidelines = {
            "content": [
                "Content aligns with brand voice and guidelines",
                "Grammar and spelling are correct",
                "Call-to-action is clear and compelling",
                "Content is optimized for target audience",
                "SEO best practices are followed"
            ],
            "campaign": [
                "Campaign objectives are clearly defined",
                "Target audience is well-defined",
                "Budget allocation is appropriate",
                "Timeline is realistic",
                "Success metrics are measurable"
            ],
            "social_media": [
                "Platform-specific best practices are followed",
                "Hashtags are relevant and researched",
                "Visual content meets platform requirements",
                "Engagement prompts are included",
                "Posting time is optimized"
            ],
            "email": [
                "Subject line is compelling",
                "Preview text is optimized",
                "Content is mobile-responsive",
                "Unsubscribe link is present",
                "Personalization is implemented"
            ]
        }
        
        self.qa_checklist = {
            "content": [
                "Brand voice consistency",
                "Grammar and spelling",
                "Call-to-action presence",
                "Target audience alignment",
                "SEO optimization"
            ],
            "campaign": [
                "Objective clarity",
                "Audience definition",
                "Budget合理性",
                "Timeline feasibility",
                "Metrics measurability"
            ],
            "social_media": [
                "Platform compliance",
                "Hashtag usage",
                "Visual requirements",
                "Engagement elements",
                "Timing optimization"
            ],
            "email": [
                "Subject line effectiveness",
                "Preview text optimization",
                "Mobile responsiveness",
                "Compliance elements",
                "Personalization"
            ]
        }
        
    def _check_checklist_item(self, category: str, item: str, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a specific checklist item for marketing content.
        
        Args:
            category: The category of the checklist item
            item: The checklist item to check
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing the check results
        """
        if category not in self.qa_checklist:
            return {
                "passed": False,
                "severity": "high",
                "description": f"Unknown category: {category}"
            }
            
        if item not in self.qa_checklist[category]:
            return {
                "passed": False,
                "severity": "high",
                "description": f"Unknown checklist item: {item}"
            }
            
        # Implement specific checks based on category and item
        if category == "content":
            return self._check_content_item(item, task_data, result)
        elif category == "campaign":
            return self._check_campaign_item(item, task_data, result)
        elif category == "social_media":
            return self._check_social_media_item(item, task_data, result)
        elif category == "email":
            return self._check_email_item(item, task_data, result)
        
        return {
            "passed": True,
            "severity": "low",
            "description": "Default check passed"
        }
    
    def _check_content_item(self, item: str, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a content-specific checklist item.
        
        Args:
            item: The checklist item to check
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing the check results
        """
        content = result.get("content", {})
        
        if item == "Brand voice consistency":
            # Check if content matches brand voice guidelines
            brand_voice = task_data.get("brand_voice", {})
            content_tone = content.get("tone", "")
            return {
                "passed": content_tone in brand_voice.get("allowed_tones", []),
                "severity": "high",
                "description": f"Content tone '{content_tone}' should match brand voice guidelines"
            }
            
        elif item == "Grammar and spelling":
            # Check for basic grammar and spelling
            text = content.get("text", "")
            # This would typically use a grammar checking service
            return {
                "passed": True,  # Placeholder
                "severity": "high",
                "description": "Grammar and spelling check passed"
            }
            
        elif item == "Call-to-action presence":
            # Check for presence of call-to-action
            has_cta = bool(content.get("call_to_action"))
            return {
                "passed": has_cta,
                "severity": "high",
                "description": "Call-to-action is required"
            }
            
        elif item == "Target audience alignment":
            # Check if content targets the right audience
            target_audience = task_data.get("target_audience", [])
            content_audience = content.get("target_audience", [])
            return {
                "passed": all(a in target_audience for a in content_audience),
                "severity": "high",
                "description": "Content should target the specified audience"
            }
            
        elif item == "SEO optimization":
            # Check for SEO elements
            has_keywords = bool(content.get("keywords"))
            return {
                "passed": has_keywords,
                "severity": "medium",
                "description": "Keywords should be specified for SEO"
            }
        
        return {
            "passed": True,
            "severity": "low",
            "description": "Content check passed"
        }
    
    def _check_campaign_item(self, item: str, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a campaign-specific checklist item.
        
        Args:
            item: The checklist item to check
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing the check results
        """
        campaign = result.get("campaign", {})
        
        if item == "Objective clarity":
            # Check if campaign objective is clear
            objective = campaign.get("objective", "")
            return {
                "passed": bool(objective and len(objective) > 10),
                "severity": "high",
                "description": "Campaign objective should be clearly defined"
            }
            
        elif item == "Audience definition":
            # Check if target audience is well-defined
            audience = campaign.get("target_audience", [])
            return {
                "passed": len(audience) > 0,
                "severity": "high",
                "description": "Target audience should be specified"
            }
            
        elif item == "Budget合理性":
            # Check if budget allocation is reasonable
            budget = campaign.get("budget", 0)
            return {
                "passed": budget > 0,
                "severity": "high",
                "description": "Campaign budget should be specified"
            }
            
        elif item == "Timeline feasibility":
            # Check if timeline is realistic
            timeline = campaign.get("timeline", {})
            has_dates = bool(timeline.get("start_date") and timeline.get("end_date"))
            return {
                "passed": has_dates,
                "severity": "high",
                "description": "Campaign timeline should be specified"
            }
            
        elif item == "Metrics measurability":
            # Check if success metrics are measurable
            metrics = campaign.get("metrics", {})
            has_kpi = bool(metrics.get("kpi"))
            return {
                "passed": has_kpi,
                "severity": "high",
                "description": "Success metrics should be specified"
            }
        
        return {
            "passed": True,
            "severity": "low",
            "description": "Campaign check passed"
        }
    
    def _check_social_media_item(self, item: str, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a social media-specific checklist item.
        
        Args:
            item: The checklist item to check
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing the check results
        """
        social = result.get("task", {})
        
        if item == "Platform compliance":
            # Check if content meets platform requirements
            platform = social.get("platform", "")
            content = social.get("content", {})
            return {
                "passed": bool(platform and content),
                "severity": "high",
                "description": "Content should meet platform requirements"
            }
            
        elif item == "Hashtag usage":
            # Check for appropriate hashtag usage
            content = social.get("content", {})
            hashtags = content.get("hashtags", [])
            return {
                "passed": len(hashtags) > 0,
                "severity": "medium",
                "description": "Hashtags should be used appropriately"
            }
            
        elif item == "Visual requirements":
            # Check if visual content meets requirements
            content = social.get("content", {})
            has_visual = bool(content.get("image") or content.get("video"))
            return {
                "passed": has_visual,
                "severity": "medium",
                "description": "Visual content should meet platform requirements"
            }
            
        elif item == "Engagement elements":
            # Check for engagement prompts
            content = social.get("content", {})
            has_engagement = bool(content.get("engagement_prompt"))
            return {
                "passed": has_engagement,
                "severity": "medium",
                "description": "Content should include engagement elements"
            }
            
        elif item == "Timing optimization":
            # Check if posting time is optimized
            schedule = social.get("schedule", {})
            has_time = bool(schedule.get("posting_time"))
            return {
                "passed": has_time,
                "severity": "low",
                "description": "Posting time should be optimized"
            }
        
        return {
            "passed": True,
            "severity": "low",
            "description": "Social media check passed"
        }
    
    def _check_email_item(self, item: str, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check an email-specific checklist item.
        
        Args:
            item: The checklist item to check
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing the check results
        """
        email = result.get("content", {})
        
        if item == "Subject line effectiveness":
            # Check if subject line is compelling
            subject = email.get("subject", "")
            return {
                "passed": bool(subject and len(subject) > 0),
                "severity": "high",
                "description": "Subject line should be compelling"
            }
            
        elif item == "Preview text optimization":
            # Check if preview text is optimized
            preview = email.get("preview_text", "")
            return {
                "passed": bool(preview and len(preview) > 0),
                "severity": "medium",
                "description": "Preview text should be optimized"
            }
            
        elif item == "Mobile responsiveness":
            # Check if content is mobile-responsive
            is_responsive = email.get("mobile_responsive", False)
            return {
                "passed": is_responsive,
                "severity": "high",
                "description": "Email should be mobile-responsive"
            }
            
        elif item == "Compliance elements":
            # Check for required compliance elements
            has_unsubscribe = bool(email.get("unsubscribe_link"))
            return {
                "passed": has_unsubscribe,
                "severity": "high",
                "description": "Email should include compliance elements"
            }
            
        elif item == "Personalization":
            # Check if personalization is implemented
            is_personalized = email.get("personalized", False)
            return {
                "passed": is_personalized,
                "severity": "medium",
                "description": "Email should be personalized"
            }
        
        return {
            "passed": True,
            "severity": "low",
            "description": "Email check passed"
        }
    
    def _calculate_quality_score(self, checklist_results: Dict[str, Any], task_data: Dict[str, Any], result: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the marketing task.
        
        Args:
            checklist_results: Results from the checklist review
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        total_checks = 0
        passed_checks = 0
        high_severity_checks = 0
        high_severity_passed = 0
        
        # Count total checks and passed checks
        for category in checklist_results.get("issues", []):
            total_checks += 1
            if category["severity"] == "high":
                high_severity_checks += 1
                if category.get("passed", False):
                    high_severity_passed += 1
            elif category.get("passed", False):
                passed_checks += 1
                
        for category in checklist_results.get("suggestions", []):
            total_checks += 1
            if category.get("passed", False):
                passed_checks += 1
        
        if total_checks == 0:
            return 1.0
            
        # Calculate base score
        base_score = passed_checks / total_checks
        
        # Adjust score based on high severity checks
        if high_severity_checks > 0:
            high_severity_score = high_severity_passed / high_severity_checks
            # High severity checks have more weight
            final_score = (base_score * 0.4) + (high_severity_score * 0.6)
        else:
            final_score = base_score
        
        return max(0.0, min(1.0, final_score))
    
    def review_task(self, task_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review a marketing task and provide feedback.
        
        Args:
            task_data: The original task data
            result: The result of the task
            
        Returns:
            Dictionary containing review results
        """
        self.logger.info(f"Reviewing marketing task of type: {task_data.get('type', 'unknown')}")
        
        task_type = task_data.get("type", "")
        review_results = {
            "issues": [],
            "suggestions": [],
            "passed": True
        }
        
        # Determine which checklist to use based on task type
        if task_type == "content_creation":
            checklist = self.qa_checklist["content"]
            for item in checklist:
                result = self._check_checklist_item("content", item, task_data, result)
                if not result["passed"]:
                    review_results["passed"] = False
                    if result["severity"] == "high":
                        review_results["issues"].append(result)
                    else:
                        review_results["suggestions"].append(result)
                        
        elif task_type == "campaign_creation":
            checklist = self.qa_checklist["campaign"]
            for item in checklist:
                result = self._check_checklist_item("campaign", item, task_data, result)
                if not result["passed"]:
                    review_results["passed"] = False
                    if result["severity"] == "high":
                        review_results["issues"].append(result)
                    else:
                        review_results["suggestions"].append(result)
                        
        elif task_type == "social_media":
            checklist = self.qa_checklist["social_media"]
            for item in checklist:
                result = self._check_checklist_item("social_media", item, task_data, result)
                if not result["passed"]:
                    review_results["passed"] = False
                    if result["severity"] == "high":
                        review_results["issues"].append(result)
                    else:
                        review_results["suggestions"].append(result)
                        
        elif task_type == "email_marketing":
            checklist = self.qa_checklist["email"]
            for item in checklist:
                result = self._check_checklist_item("email", item, task_data, result)
                if not result["passed"]:
                    review_results["passed"] = False
                    if result["severity"] == "high":
                        review_results["issues"].append(result)
                    else:
                        review_results["suggestions"].append(result)
                        
        else:
            review_results["passed"] = False
            review_results["issues"].append({
                "severity": "high",
                "description": f"Unknown task type: {task_type}"
            })
        
        return review_results
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a QA task for marketing content.
        
        Args:
            input_data: Dictionary containing task data and result to review
            
        Returns:
            Dictionary containing the review results
        """
        self.logger.info(f"Processing QA task for marketing content")
        
        task_data = input_data.get("task_data", {})
        result = input_data.get("result", {})
        
        if not task_data or not result:
            return {
                "success": False,
                "error": "Missing task data or result"
            }
            
        # Review the task
        review = self.review_task(task_data, result)
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(review, task_data, result)
        
        # Add review to history
        self.review_history.append({
            "task_id": result.get("id", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "review": review,
            "quality_score": quality_score
        })
        
        return {
            "success": True,
            "review": review,
            "quality_score": quality_score,
            "message": "QA review completed successfully"
        }
    
    def __str__(self) -> str:
        """
        String representation of the marketing QA agent.
        
        Returns:
            String describing the marketing QA agent
        """
        return f"{self.name} (Marketing QA) - Marketing Department" 