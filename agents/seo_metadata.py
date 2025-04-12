from typing import Dict, Any, List
from .base_agent import BaseAgent

class SEOMetadataAgent(BaseAgent):
    async def generate_titles(self, concept: Dict[str, Any], script: Dict[str, Any]) -> List[str]:
        """
        Generate SEO-optimized titles for the video
        """
        title_prompt = f"""
        Based on the following video concept and script, generate 5 SEO-optimized titles for YouTube:
        Concept: {concept}
        Script: {script}
        
        Requirements:
        1. Each title should be under 60 characters
        2. Include relevant keywords
        3. Be attention-grabbing and clickable
        4. Avoid clickbait
        5. Follow YouTube best practices
        
        Format the response as a JSON array of strings.
        """
        
        titles_response = await self.get_completion(title_prompt)
        try:
            # Simple parsing - in a real implementation, you would use proper JSON parsing
            titles = [title.strip() for title in titles_response.strip('[]').split(',')]
            return titles
        except Exception as e:
            print(f"Error parsing titles: {str(e)}")
            return ["Untitled Video"]
    
    async def generate_tags(self, concept: Dict[str, Any], description: str) -> List[str]:
        """
        Generate relevant tags for the video
        """
        tags_prompt = f"""
        Based on the following video concept and description, generate 15 relevant tags for YouTube:
        Concept: {concept}
        Description: {description}
        
        Requirements:
        1. Include a mix of specific and general tags
        2. Use trending keywords where relevant
        3. Include variations of important terms
        4. Follow YouTube tag best practices
        
        Format the response as a JSON array of strings.
        """
        
        tags_response = await self.get_completion(tags_prompt)
        try:
            # Simple parsing - in a real implementation, you would use proper JSON parsing
            tags = [tag.strip() for tag in tags_response.strip('[]').split(',')]
            return tags
        except Exception as e:
            print(f"Error parsing tags: {str(e)}")
            return ["video", "youtube"]
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the SEO metadata request
        """
        concept = input_data.get("concept", {})
        script = input_data.get("script", {})
        description = input_data.get("description", "")
        
        # Generate titles
        titles = await self.generate_titles(concept, script)
        
        # Generate tags
        tags = await self.generate_tags(concept, description)
        
        return {
            "titles": titles,
            "tags": tags,
            "status": "success"
        } 