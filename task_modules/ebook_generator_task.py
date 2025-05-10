import os
import json
import logging
import tempfile
from dotenv import load_dotenv
from .ebook_generator import EbookGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EbookGeneratorTask:
    """
    Task module for generating ebooks using the EbookGenerator class.
    This class is designed to be called by the Agent Core Service.
    """
    
    def __init__(self):
        """
        Initialize the EbookGeneratorTask.
        The API key is loaded from environment variables when execute() is called.
        """
        self.api_key = None
        self.generator = None
        logger.info("EbookGeneratorTask initialized")
    
    def execute(self, parameters):
        """
        Execute the ebook generation task with the provided parameters.
        
        Args:
            parameters (google.protobuf.Struct): Parameters for the ebook generation task.
                Expected fields:
                - topic: The main topic of the book
                - audience: The target audience for the book
                - num_chapters: (Optional) Number of chapters to generate
        
        Returns:
            dict: A dictionary containing the task result with the following fields:
                - status: "completed" or "failed"
                - result: (If completed) Information about the generated ebook
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
            else:
                # Handle regular dict (for testing)
                params = parameters
            
            logger.info(f"Executing ebook generation task with parameters: {params}")
            
            # Validate required parameters
            if 'topic' not in params:
                return {"status": "failed", "message": "Missing required parameter: topic"}
            if 'audience' not in params:
                return {"status": "failed", "message": "Missing required parameter: audience"}
            
            # Get parameters
            topic = params['topic']
            audience = params['audience']
            num_chapters = int(params.get('num_chapters', 5))  # Default to 5 chapters
            
            # Get API key from environment
            self.api_key = os.getenv('ABACUSAI_API_KEY')
            if not self.api_key:
                return {"status": "failed", "message": "ABACUSAI_API_KEY not found in environment variables"}
            
            # Initialize generator
            self.generator = EbookGenerator(self.api_key)
            
            # Create temporary directory for output
            with tempfile.TemporaryDirectory() as temp_dir:
                logger.info(f"Generating ebook in temporary directory: {temp_dir}")
                
                # Generate the book
                self.generator.generate_full_book(topic, audience, temp_dir, num_chapters)
                
                # Read the outline
                outline_path = os.path.join(temp_dir, 'outline.json')
                if not os.path.exists(outline_path):
                    return {"status": "failed", "message": "Failed to generate book outline"}
                
                with open(outline_path, 'r') as f:
                    outline = json.load(f)
                
                # Get chapter information
                chapters = []
                chapters_dir = os.path.join(temp_dir, 'chapters')
                if os.path.exists(chapters_dir):
                    for chapter in outline['chapters']:
                        chapter_file = os.path.join(chapters_dir, f"chapter_{chapter['number']:02d}.md")
                        if os.path.exists(chapter_file):
                            with open(chapter_file, 'r') as f:
                                chapter_content = f.read()
                            chapters.append({
                                "number": chapter['number'],
                                "title": chapter['title'],
                                "content_length": len(chapter_content),
                                "content_preview": chapter_content[:200] + "..." if len(chapter_content) > 200 else chapter_content
                            })
                
                # Return success result
                return {
                    "status": "completed",
                    "result": {
                        "title": outline['title'],
                        "description": outline['description'],
                        "num_chapters": len(outline['chapters']),
                        "chapters_generated": len(chapters),
                        "chapters": chapters
                    }
                }
                
        except Exception as e:
            logger.error(f"Error executing ebook generation task: {e}", exc_info=True)
            return {"status": "failed", "message": f"Error executing ebook generation task: {str(e)}"}
