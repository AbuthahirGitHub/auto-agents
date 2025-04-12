from typing import Dict, Any, List
import os
import subprocess
from .base_agent import BaseAgent

class VideoEditorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def combine_videos(self, video_paths: List[str], output_path: str) -> str:
        """
        Combine multiple videos using ffmpeg
        """
        try:
            # Create a file list for ffmpeg
            list_file = os.path.join(self.output_dir, "filelist.txt")
            with open(list_file, "w") as f:
                for path in video_paths:
                    f.write(f"file '{path}'\n")
            
            # Use ffmpeg to concatenate videos
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c", "copy",
                output_path
            ]
            subprocess.run(cmd, check=True)
            
            # Clean up
            os.remove(list_file)
            
            return output_path
        except Exception as e:
            print(f"Error combining videos: {str(e)}")
            return ""
    
    async def add_text_overlay(self, video_path: str, text: str, position: str = "center", output_path: str = None) -> str:
        """
        Add text overlay to a video using ffmpeg
        """
        try:
            if output_path is None:
                output_path = f"{os.path.splitext(video_path)[0]}_with_text.mp4"
            
            # Use ffmpeg to add text overlay
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-vf", f"drawtext=text='{text}':fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-10",
                "-codec:a", "copy",
                output_path
            ]
            subprocess.run(cmd, check=True)
            
            return output_path
        except Exception as e:
            print(f"Error adding text overlay: {str(e)}")
            return video_path
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the video editing request
        """
        videos = input_data.get("videos", [])
        script = input_data.get("script", {})
        voiceover = input_data.get("voiceover", {})
        
        if not videos:
            return {
                "status": "error",
                "message": "No videos provided for editing"
            }
        
        # Extract video paths
        video_paths = [video.get("filepath", "") for video in videos if video.get("filepath")]
        
        if not video_paths:
            return {
                "status": "error",
                "message": "No valid video paths found"
            }
        
        # Generate output filename
        output_filename = f"final_video_{os.path.basename(video_paths[0]).split('_')[0]}.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Combine videos
        combined_video = await self.combine_videos(video_paths, output_path)
        
        if not combined_video:
            return {
                "status": "error",
                "message": "Failed to combine videos"
            }
        
        # Add text overlays based on script
        if script:
            # This is a simplified version - in a real implementation, you would parse the script
            # and add text overlays at specific timestamps
            text_output = await self.add_text_overlay(
                combined_video, 
                "Created with AI Video Creation System", 
                "bottom", 
                f"{os.path.splitext(combined_video)[0]}_with_text.mp4"
            )
            
            if text_output:
                combined_video = text_output
        
        return {
            "output_path": combined_video,
            "status": "success"
        } 