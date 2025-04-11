# AI Video Creation System

An automated YouTube video creation system powered by multiple AI agents. This system creates engaging videos using Pexels stock footage with a single click.

## AI Agents

1. **Content Strategist Agent**
   - Generates video concepts and themes
   - Determines target audience and content strategy
   - Creates video outlines and scripts

2. **Video Searcher Agent**
   - Searches and selects relevant stock videos from Pexels
   - Ensures video quality and relevance
   - Manages video metadata and licensing

3. **Script Writer Agent**
   - Generates engaging scripts based on content strategy
   - Creates voiceover scripts
   - Optimizes for SEO and engagement

4. **Video Editor Agent**
   - Combines selected videos
   - Adds transitions and effects
   - Handles video rendering and export

5. **SEO & Metadata Agent**
   - Generates optimized titles and descriptions
   - Creates tags and metadata
   - Suggests thumbnails and end screens

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
PEXELS_API_KEY=your_pexels_api_key
OPENAI_API_KEY=your_openai_api_key
```

3. Run the application:
```bash
python main.py
```

## Usage

1. Access the web interface at `http://localhost:8000`
2. Enter your video topic or theme
3. Click "Generate Video"
4. Wait for the AI agents to create your video
5. Download the final video

## Project Structure

```
├── agents/
│   ├── content_strategist.py
│   ├── video_searcher.py
│   ├── script_writer.py
│   ├── video_editor.py
│   └── seo_metadata.py
├── utils/
│   ├── video_processor.py
│   ├── api_client.py
│   └── config.py
├── main.py
├── requirements.txt
└── .env
``` 