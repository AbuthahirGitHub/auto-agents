from typing import Dict, Any
from .base_agent import BaseAgent

class ContentStrategistAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate video concept and strategy based on the input topic
        """
        topic = input_data.get("topic", "")
        
        # Generate video concept
        concept_prompt = f"""
        Create a detailed video concept for a YouTube video about: {topic}
        
        Include:
        1. Target audience
        2. Main message/theme
        3. Key points to cover
        4. Suggested video length
        5. Visual style recommendations
        6. Emotional tone
        7. Call to action
        
        Format the response as a structured JSON.
        """
        
        concept_response = await self.get_completion(concept_prompt)
        
        # Generate content strategy
        strategy_prompt = f"""
        Based on the following video concept, create a detailed content strategy:
        {concept_response}
        
        Include:
        1. Hook/opening sequence
        2. Main content structure
        3. Visual transitions
        4. Music/sound recommendations
        5. Engagement points
        6. SEO optimization strategy
        
        Format the response as a structured JSON.
        """
        
        strategy_response = await self.get_completion(strategy_prompt)
        
        return {
            "concept": concept_response,
            "strategy": strategy_response,
            "status": "success"
        } 