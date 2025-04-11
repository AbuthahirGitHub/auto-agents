import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from agents.content_strategist import ContentStrategistAgent
from agents.video_searcher import VideoSearcherAgent
from agents.script_writer import ScriptWriterAgent
from agents.video_editor import VideoEditorAgent
from agents.seo_metadata import SEOMetadataAgent

app = FastAPI(title="AI Video Creation System")

class VideoRequest(BaseModel):
    topic: str
    keywords: Optional[List[str]] = []
    style: Optional[str] = "professional"
    duration: Optional[int] = 300  # in seconds

class VideoResponse(BaseModel):
    video_path: str
    title: str
    description: str
    tags: List[str]
    status: str
    message: Optional[str] = None

async def create_video(request: VideoRequest) -> VideoResponse:
    try:
        # Initialize agents
        content_agent = ContentStrategistAgent()
        video_agent = VideoSearcherAgent()
        script_agent = ScriptWriterAgent()
        editor_agent = VideoEditorAgent()
        seo_agent = SEOMetadataAgent()
        
        # Step 1: Generate content strategy
        content_result = await content_agent.process({
            "topic": request.topic,
            "keywords": request.keywords,
            "style": request.style
        })
        
        if content_result["status"] != "success":
            raise Exception("Failed to generate content strategy")
        
        # Step 2: Search and download videos
        video_result = await video_agent.process({
            "concept": content_result["concept"],
            "keywords": request.keywords
        })
        
        if video_result["status"] != "success":
            raise Exception("Failed to find suitable videos")
        
        # Step 3: Generate script and voiceover
        script_result = await script_agent.process({
            "concept": content_result["concept"],
            "strategy": content_result["strategy"],
            "videos": video_result["videos"]
        })
        
        if script_result["status"] != "success":
            raise Exception("Failed to generate script")
        
        # Step 4: Edit video
        editor_result = await editor_agent.process({
            "videos": video_result["videos"],
            "script": script_result["script"],
            "voiceover": script_result["voiceover"]
        })
        
        if editor_result["status"] != "success":
            raise Exception("Failed to edit video")
        
        # Step 5: Generate SEO metadata
        seo_result = await seo_agent.process({
            "concept": content_result["concept"],
            "script": script_result["script"],
            "description": script_result["description"]
        })
        
        if seo_result["status"] != "success":
            raise Exception("Failed to generate SEO metadata")
        
        return VideoResponse(
            video_path=editor_result["output_path"],
            title=seo_result["titles"][0],  # Use the first suggested title
            description=script_result["description"],
            tags=seo_result["tags"],
            status="success"
        )
        
    except Exception as e:
        return VideoResponse(
            video_path="",
            title="",
            description="",
            tags=[],
            status="error",
            message=str(e)
        )

@app.post("/create-video", response_model=VideoResponse)
async def create_video_endpoint(request: VideoRequest):
    result = await create_video(request)
    if result.status == "error":
        raise HTTPException(status_code=500, detail=result.message)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 