from typing import Dict, Any
from .base_agent import BaseAgent

class ScriptWriterAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate video script and voiceover based on content strategy
        """
        concept = input_data.get("concept", {})
        strategy = input_data.get("strategy", {})
        videos = input_data.get("videos", [])
        
        # Generate main script
        script_prompt = f"""
        Create a detailed video script based on:
        Concept: {concept}
        Strategy: {strategy}
        Available Videos: {len(videos)} clips
        
        Include:
        1. Opening hook (5-7 seconds)
        2. Main content sections
        3. Transitions between sections
        4. Closing call to action
        
        Format as a JSON with timestamps and sections.
        """
        
        script_response = await self.get_completion(script_prompt)
        
        # Generate voiceover script
        voiceover_prompt = f"""
        Based on the following script, create a natural, engaging voiceover script:
        {script_response}
        
        Requirements:
        1. Conversational tone
        2. Clear pronunciation guides
        3. Timing markers
        4. Emotional cues
        5. Breathing/pause markers
        
        Format as a JSON with timestamps and text.
        """
        
        voiceover_response = await self.get_completion(voiceover_prompt)
        
        # Generate SEO-optimized description
        description_prompt = f"""
        Create an SEO-optimized video description based on:
        Script: {script_response}
        
        Include:
        1. Compelling first 2-3 lines
        2. Key points covered
        3. Relevant hashtags
        4. Call to action
        5. Links and timestamps
        
        Format as a JSON with sections.
        """
        
        description_response = await self.get_completion(description_prompt)
        
        return {
            "script": script_response,
            "voiceover": voiceover_response,
            "description": description_response,
            "status": "success"
        } 