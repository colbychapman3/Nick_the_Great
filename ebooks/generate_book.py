import os
import json
import logging
from dotenv import load_dotenv
from abacusai import ApiClient
from google.protobuf.struct_pb2 import Struct

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class EbookGeneratorTask:
    """
    Task module for generating ebooks using AbacusAI.
    """
    def __init__(self):
        """
        Initializes the AbacusAI client.
        """
        api_key = os.getenv('ABACUSAI_API_KEY')
        if not api_key:
            logger.error("ABACUSAI_API_KEY not found in environment variables")
            self.client = None
        else:
            try:
                self.client = ApiClient(api_key)
            except Exception as e:
                logger.error(f"Failed to initialize AbacusAI client: {e}")
                self.client = None

    def execute(self, parameters: Struct) -> dict:
        """
        Executes the ebook generation task.

        Args:
            parameters (Struct): A protobuf Struct containing task parameters
                                 (e.g., topic, audience, num_chapters).

        Returns:
            dict: A dictionary containing the generated book outline and content,
                  or None if an error occurred.
        """
        if not self.client:
            logger.error("AbacusAI client not initialized. Cannot execute task.")
            return {"status": "failed", "message": "AbacusAI client not initialized"}

        params = {key: value for key, value in parameters.items()}
        topic = params.get("topic")
        audience = params.get("audience")
        num_chapters = params.get("num_chapters", 10)

        if not topic or not audience:
            logger.error("Missing required parameters: topic or audience")
            return {"status": "failed", "message": "Missing required parameters: topic or audience"}

        logger.info(f"Generating book outline for '{topic}' targeted at {audience}...")
        outline = self._generate_book_outline(topic, audience, num_chapters)

        if not outline:
            logger.error("Failed to generate book outline.")
            return {"status": "failed", "message": "Failed to generate book outline"}

        logger.info(f"Book outline generated: {outline.get('title', 'Untitled Book')}")

        book_content = {"outline": outline, "chapters": []}

        for chapter in outline.get('chapters', []):
            logger.info(f"Generating Chapter {chapter.get('number', 'N/A')}: {chapter.get('title', 'Untitled Chapter')}...")
            content = self._generate_chapter_content(outline.get('title', 'Untitled Book'), chapter, audience)

            if content:
                book_content["chapters"].append({
                    "number": chapter.get('number'),
                    "title": chapter.get('title'),
                    "content": content
                })
                logger.info(f"Chapter {chapter.get('number', 'N/A')} content generated.")
            else:
                logger.error(f"Failed to generate content for Chapter {chapter.get('number', 'N/A')}.")
                # Decide if failure to generate one chapter should fail the whole task
                # For now, we'll continue and return partial results

        return {"status": "completed", "result": book_content}

    def _generate_book_outline(self, topic, audience, num_chapters):
        """
        Generate a book outline with chapter titles and brief descriptions.
        Internal helper method.
        """
        prompt = f"""
        Create a detailed outline for a non-fiction book about {topic} specifically targeted at {audience}.

        The book should have a catchy, marketable title and approximately {num_chapters} chapters.

        For each chapter, provide:
        1. A compelling chapter title
        2. A brief description of what the chapter will cover (2-3 sentences)

        Also include a compelling book description that would attract readers from the target audience.

        Format the response as a JSON object with the following structure:
        {{
            "title": "Book Title",
            "description": "Overall book description",
            "chapters": [
                {{
                    "number": 1,
                    "title": "Chapter Title",
                    "description": "Brief chapter description"
                }},
                ...
            ]
        }}
        """

        try:
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7,
                model="claude-3-opus-20240229" # Using a specific model as per original script
            )

            # Parse the JSON response
            outline = json.loads(response.generations[0].text)
            return outline
        except Exception as e:
            logger.error(f"Error generating book outline: {e}")
            return None

    def _generate_chapter_content(self, book_title, chapter_info, audience):
        """
        Generate content for a specific chapter.
        Internal helper method.
        """
        prompt = f"""
        Write chapter {chapter_info.get('number', 'N/A')} titled "{chapter_info.get('title', 'Untitled Chapter')}" for a book called "{book_title}" targeted at {audience}.

        Chapter description: {chapter_info.get('description', '')}

        The content should be engaging, informative, and tailored specifically for {audience}.
        Include relevant examples, research findings, and practical advice where appropriate.

        Structure the chapter with clear sections, subheadings, and a logical flow.

        Write approximately 2000-3000 words of high-quality content that would be valuable enough for someone to pay for.
        """

        try:
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=4000, # Increased max_tokens for potentially longer chapters
                temperature=0.7,
                model="claude-3-opus-20240229" # Using a specific model
            )

            return response.generations[0].text
        except Exception as e:
            logger.error(f"Error generating chapter content: {e}")
            return None

# Example usage (for testing the module directly if needed)
if __name__ == "__main__":
    # This part is for direct testing and can be removed or kept for utility
    # It mimics how the Agent Core might call the task
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    task = EbookGeneratorTask()

    # Create a dummy parameters Struct
    params_struct = Struct()
    params_struct.update({
        "topic": "Artificial Intelligence in Business",
        "audience": "Small Business Owners",
        "num_chapters": 5
    })

    result = task.execute(params_struct)
    print("\nTask Result:")
    print(json.dumps(result, indent=2))

    # Example of missing parameters
    print("\nTesting with missing parameters:")
    params_struct_missing = Struct()
    params_struct_missing.update({
        "topic": "Another Topic"
        # audience is missing
    })
    result_missing = task.execute(params_struct_missing)
    print(json.dumps(result_missing, indent=2))
