import os
import json
import logging
import tempfile
from dotenv import load_dotenv
from abacusai import ApiClient

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FreelanceWritingTask:
    """
    Task module for managing freelance writing projects.
    This class is designed to be called by the Agent Core Service.
    """
    
    def __init__(self):
        """
        Initialize the FreelanceWritingTask.
        The API key is loaded from environment variables when execute() is called.
        """
        self.api_key = None
        self.client = None
        logger.info("FreelanceWritingTask initialized")
    
    def execute(self, parameters):
        """
        Execute the freelance writing task with the provided parameters.
        
        Args:
            parameters (google.protobuf.Struct): Parameters for the freelance writing task.
                Expected fields:
                - project_type: Type of writing project (article, blog post, etc.)
                - topic: The main topic of the writing project
                - target_audience: The target audience for the content
                - word_count: (Optional) Target word count
                - tone: (Optional) Desired tone of the content
                - keywords: (Optional) List of keywords to include
        
        Returns:
            dict: A dictionary containing the task result with the following fields:
                - status: "completed" or "failed"
                - result: (If completed) Information about the generated content
                - message: (If failed) Error message
        """
        try:
            # Convert protobuf Struct to Python dict
            params = {}
            if hasattr(parameters, 'fields'):
                # Handle protobuf Struct
                for key, value in parameters.fields.items():
                    if hasattr(value, 'string_value'):
                        params[key] = value.string_value
                    elif hasattr(value, 'number_value'):
                        params[key] = value.number_value
                    elif hasattr(value, 'bool_value'):
                        params[key] = value.bool_value
                    elif hasattr(value, 'list_value') and hasattr(value.list_value, 'values'):
                        params[key] = [v.string_value for v in value.list_value.values]
            else:
                # Handle regular dict (for testing)
                params = parameters
            
            logger.info(f"Executing freelance writing task with parameters: {params}")
            
            # Validate required parameters
            if 'project_type' not in params:
                return {"status": "failed", "message": "Missing required parameter: project_type"}
            if 'topic' not in params:
                return {"status": "failed", "message": "Missing required parameter: topic"}
            if 'target_audience' not in params:
                return {"status": "failed", "message": "Missing required parameter: target_audience"}
            
            # Get parameters
            project_type = params['project_type']
            topic = params['topic']
            target_audience = params['target_audience']
            word_count = int(params.get('word_count', 1000))  # Default to 1000 words
            tone = params.get('tone', 'professional')
            keywords = params.get('keywords', [])
            
            # Get API key from environment
            self.api_key = os.getenv('ABACUSAI_API_KEY')
            if not self.api_key:
                return {"status": "failed", "message": "ABACUSAI_API_KEY not found in environment variables"}
            
            # Initialize AbacusAI client
            self.client = ApiClient(self.api_key)
            
            # Generate content outline
            outline = self._generate_content_outline(project_type, topic, target_audience, word_count, tone, keywords)
            if not outline:
                return {"status": "failed", "message": "Failed to generate content outline"}
            
            # Generate full content
            content = self._generate_full_content(outline, project_type, topic, target_audience, word_count, tone, keywords)
            if not content:
                return {"status": "failed", "message": "Failed to generate full content"}
            
            # Create temporary directory for output
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save content to file
                content_file = os.path.join(temp_dir, f"{topic.replace(' ', '_').lower()}.md")
                with open(content_file, 'w') as f:
                    f.write(content)
                
                # Save metadata
                metadata = {
                    "project_type": project_type,
                    "topic": topic,
                    "target_audience": target_audience,
                    "word_count": word_count,
                    "tone": tone,
                    "keywords": keywords,
                    "content_length": len(content),
                    "content_preview": content[:200] + "..." if len(content) > 200 else content
                }
                
                metadata_file = os.path.join(temp_dir, "metadata.json")
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                # Return success result
                return {
                    "status": "completed",
                    "result": {
                        "project_type": project_type,
                        "topic": topic,
                        "target_audience": target_audience,
                        "word_count": word_count,
                        "tone": tone,
                        "keywords": keywords,
                        "content_length": len(content),
                        "content_preview": content[:200] + "..." if len(content) > 200 else content
                    }
                }
                
        except Exception as e:
            logger.error(f"Error executing freelance writing task: {e}", exc_info=True)
            return {"status": "failed", "message": f"Error executing freelance writing task: {str(e)}"}
    
    def _generate_content_outline(self, project_type, topic, target_audience, word_count, tone, keywords):
        """
        Generate an outline for the content.
        
        Returns:
            dict: Outline structure or None on error
        """
        try:
            # Prepare keywords string
            keywords_str = ", ".join(keywords) if keywords else "no specific keywords required"
            
            prompt = f"""
            Create a detailed outline for a {project_type} about {topic} targeted at {target_audience}.
            The content should be approximately {word_count} words and written in a {tone} tone.
            Please include these keywords where appropriate: {keywords_str}.
            
            Format the response as a JSON object with the following structure:
            {{
                "title": "Compelling title for the {project_type}",
                "introduction": "Brief description of the introduction section",
                "sections": [
                    {{
                        "heading": "Section heading",
                        "subheadings": [
                            "Subheading 1",
                            "Subheading 2"
                        ],
                        "key_points": [
                            "Key point 1",
                            "Key point 2"
                        ]
                    }}
                ],
                "conclusion": "Brief description of the conclusion section"
            }}
            """
            
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7,
                model="claude-3-opus-20240229"
            )
            
            # Parse the JSON response
            outline = json.loads(response.generations[0].text)
            logger.info(f"Generated content outline for {project_type} on topic: {topic}")
            return outline
            
        except Exception as e:
            logger.error(f"Error generating content outline: {e}", exc_info=True)
            return None
    
    def _generate_full_content(self, outline, project_type, topic, target_audience, word_count, tone, keywords):
        """
        Generate the full content based on the outline.
        
        Returns:
            str: Generated content or None on error
        """
        try:
            # Prepare keywords string
            keywords_str = ", ".join(keywords) if keywords else "no specific keywords required"
            
            # Convert outline to string representation
            outline_str = json.dumps(outline, indent=2)
            
            prompt = f"""
            Write a complete {project_type} about {topic} targeted at {target_audience}, following this outline:
            
            {outline_str}
            
            The content should be:
            - Approximately {word_count} words
            - Written in a {tone} tone
            - Include these keywords where appropriate: {keywords_str}
            - Well-structured with clear headings and subheadings
            - Engaging and valuable to the target audience
            - Formatted in Markdown
            
            Please provide the complete, ready-to-publish content.
            """
            
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=4000,
                temperature=0.7,
                model="claude-3-opus-20240229"
            )
            
            content = response.generations[0].text
            logger.info(f"Generated full content for {project_type} on topic: {topic}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating full content: {e}", exc_info=True)
            return None
