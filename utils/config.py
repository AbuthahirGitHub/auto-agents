import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Video Settings
    MAX_VIDEO_DURATION = 600  # 10 minutes
    DEFAULT_VIDEO_QUALITY = "1080p"
    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"
    
    # API Settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    @classmethod
    def validate(cls):
        """
        Validate required environment variables
        """
        missing_vars = []
        
        if not cls.PEXELS_API_KEY:
            missing_vars.append("PEXELS_API_KEY")
        if not cls.OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Create required directories
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True) 