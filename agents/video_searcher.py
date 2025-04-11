from typing import Dict, Any, List
import os
import requests
from .base_agent import BaseAgent

class VideoSearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
        self.headers = {"Authorization": self.pexels_api_key}
        
    async def search_videos(self, query: str, per_page: int = 5) -> List[Dict]:
        """
        Search videos on Pexels
        """
        url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("videos", [])
        return []
    
    async def download_video(self, video_url: str, filename: str) -> str:
        """
        Download a video from Pexels
        """
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            os.makedirs("downloads", exist_ok=True)
            filepath = os.path.join("downloads", filename)
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return filepath
        return ""
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the video search request
        """
        concept = input_data.get("concept", {})
        keywords = input_data.get("keywords", [])
        
        # Generate search queries based on concept and keywords
        search_prompt = f"""
        Based on the following video concept and keywords, generate 3 specific search queries for stock videos:
        Concept: {concept}
        Keywords: {keywords}
        
        Format the response as a comma-separated list of queries.
        """
        
        search_queries = (await self.get_completion(search_prompt)).split(",")
        
        all_videos = []
        for query in search_queries:
            videos = await self.search_videos(query.strip())
            all_videos.extend(videos)
        
        # Download the best quality videos
        downloaded_videos = []
        for video in all_videos:
            best_quality = max(video["video_files"], key=lambda x: x["height"])
            filename = f"{video['id']}_{best_quality['quality']}.mp4"
            filepath = await self.download_video(best_quality["link"], filename)
            if filepath:
                downloaded_videos.append({
                    "id": video["id"],
                    "filepath": filepath,
                    "duration": video["duration"],
                    "width": best_quality["width"],
                    "height": best_quality["height"]
                })
        
        return {
            "videos": downloaded_videos,
            "status": "success" if downloaded_videos else "error"
        } 