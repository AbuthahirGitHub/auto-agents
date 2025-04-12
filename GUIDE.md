# Video Creation Guide

This guide will walk you through the process of setting up and using the AI Video Creation System to generate videos with a single click.

## Prerequisites

Before you begin, make sure you have:

1. Python 3.8 or higher installed
2. A Pexels API key (for stock footage)
3. An OpenAI API key (for content generation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
PEXELS_API_KEY=your_pexels_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Starting the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. The server will start running at `http://localhost:8000`

## Creating a Video

### Using the Web Interface

1. Open your web browser and navigate to `http://localhost:8000`
2. You'll see a form where you can enter:
   - **Topic**: The main subject of your video
   - **Keywords**: Optional keywords to guide the content
   - **Style**: The tone of the video (default: "professional")
   - **Duration**: The desired length in seconds (default: 300 seconds / 5 minutes)
3. Click "Generate Video" and wait for the process to complete
4. Once finished, you'll receive:
   - The path to your generated video
   - A suggested title
   - A description
   - Recommended tags

### Using the API Directly

You can also create videos programmatically by sending a POST request to the API:

```python
import requests
import json

url = "http://localhost:8000/create-video"
payload = {
    "topic": "Artificial Intelligence in Healthcare",
    "keywords": ["AI", "healthcare", "medical technology", "future of medicine"],
    "style": "educational",
    "duration": 240
}

response = requests.post(url, json=payload)
result = response.json()

if result["status"] == "success":
    print(f"Video created successfully!")
    print(f"Title: {result['title']}")
    print(f"Description: {result['description']}")
    print(f"Tags: {result['tags']}")
    print(f"Video saved to: {result['video_path']}")
else:
    print(f"Error: {result['message']}")
```

## How It Works

The system uses five specialized AI agents to create your video:

1. **Content Strategist Agent**
   - Analyzes your topic and keywords
   - Develops a content strategy
   - Creates a video outline

2. **Video Searcher Agent**
   - Searches Pexels for relevant stock footage
   - Downloads and organizes the videos
   - Ensures quality and relevance

3. **Script Writer Agent**
   - Generates a script based on the content strategy
   - Creates a voiceover script
   - Optimizes for engagement

4. **Video Editor Agent**
   - Combines the selected videos
   - Adds transitions and effects
   - Renders the final video

5. **SEO & Metadata Agent**
   - Generates optimized titles and descriptions
   - Creates relevant tags
   - Suggests thumbnails

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your API keys are correctly set in the `.env` file
   - Check that the keys have sufficient permissions

2. **Video Generation Failures**
   - Check the server logs for specific error messages
   - Ensure you have sufficient disk space for video processing
   - Verify your internet connection for downloading stock footage

3. **Performance Issues**
   - For longer videos, the process may take several minutes
   - Consider reducing the duration for faster results

### Getting Help

If you encounter issues not covered in this guide:
1. Check the project's issue tracker
2. Contact the development team
3. Refer to the documentation in the `docs/` directory

## Advanced Usage

### Customizing Video Styles

You can specify different styles for your videos:
- `professional`: Formal, business-oriented content
- `casual`: Relaxed, conversational tone
- `educational`: Clear, instructional approach
- `entertaining`: Engaging, fun content

### Batch Processing

For creating multiple videos, you can use the batch processing feature:

```python
import asyncio
import aiohttp

async def create_multiple_videos(topics):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for topic in topics:
            payload = {
                "topic": topic,
                "style": "professional",
                "duration": 180
            }
            tasks.append(session.post("http://localhost:8000/create-video", json=payload))
        
        responses = await asyncio.gather(*tasks)
        return [await response.json() for response in responses]

# Example usage
topics = [
    "Introduction to Machine Learning",
    "The Future of Renewable Energy",
    "Digital Marketing Strategies"
]

results = asyncio.run(create_multiple_videos(topics))
```

## License

This guide is part of the AI Video Creation System and is licensed under the same terms as the main project. 