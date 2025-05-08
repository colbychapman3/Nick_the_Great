import os
import json
import logging
from abacusai import ApiClient
from dotenv import load_dotenv

# Load environment variables (if running as a standalone script)
if __name__ == "__main__":
    load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EbookGenerator:
    def __init__(self, api_key):
        """
        Initializes the EbookGenerator with the AbacusAI API key.

        Args:
            api_key (str): The AbacusAI API key.
        """
        self.api_key = api_key
        self.client = ApiClient(self.api_key)
        logging.info("EbookGenerator initialized")

    def generate_book_outline(self, topic, audience, num_chapters=10):
        """
        Generates a book outline with chapter titles and brief descriptions.

        Args:
            topic (str): The main topic of the book.
            audience (str): The target audience for the book.
            num_chapters (int): Number of chapters to generate.

        Returns:
            dict: Book outline with title, description, and chapters, or None on error.
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
                model="claude-3-opus-20240229"
            )

            # Parse the JSON response
            outline = json.loads(response.generations[0].text)
            logging.info(f"Generated book outline for topic: {topic}")
            return outline
        except Exception as e:
            logging.error(f"Error generating book outline: {e}")
            return None

    def generate_chapter_content(self, book_title, chapter_info, audience):
        """
        Generates content for a specific chapter.

        Args:
            book_title (str): The title of the book.
            chapter_info (dict): Chapter information including number, title, and description.
            audience (str): The target audience for the book.

        Returns:
            str: Generated chapter content, or None on error.
        """
        prompt = f"""
        Write chapter {chapter_info['number']} titled "{chapter_info['title']}" for a book called "{book_title}" targeted at {audience}.

        Chapter description: {chapter_info['description']}

        The content should be engaging, informative, and tailored specifically for {audience}.
        Include relevant examples, research findings, and practical advice where appropriate.

        Structure the chapter with clear sections, subheadings, and a logical flow.

        Write approximately 2000-3000 words of high-quality content that would be valuable enough for someone to pay for.
        """

        try:
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=4000,
                temperature=0.7,
                model="claude-3-opus-20240229"
            )

            logging.info(f"Generated chapter content: {chapter_info['title']}")
            return response.generations[0].text
        except Exception as e:
            logging.error(f"Error generating chapter content: {e}")
            return None

    def generate_full_book(self, topic, audience, output_dir, num_chapters=10):
        """
        Generates a complete book including outline and all chapters.

        Args:
            topic (str): The main topic of the book.
            audience (str): The target audience for the book.
            output_dir (str): The directory to save the generated files.
            num_chapters (int): Number of chapters to generate.
        """
        logging.info(f"Generating book outline for '{topic}' targeted at {audience}...")
        outline = self.generate_book_outline(topic, audience, num_chapters)

        if not outline:
            logging.error("Failed to generate book outline. Exiting.")
            return

        logging.info(f"Book outline generated: {outline['title']}")
        self.save_outline(outline, output_dir)

        for chapter in outline['chapters']:
            logging.info(f"Generating Chapter {chapter['number']}: {chapter['title']}...")
            content = self.generate_chapter_content(outline['title'], chapter, audience)

            if content:
                self.save_chapter(content, output_dir, chapter['number'])
                logging.info(f"Chapter {chapter['number']} completed and saved.")
            else:
                logging.error(f"Failed to generate content for Chapter {chapter['number']}.")

        logging.info(f"Book generation complete. Files saved to {output_dir}")

    def save_outline(self, outline, output_dir):
        """Saves the book outline to a JSON and markdown file."""
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'outline.json'), 'w') as f:
            json.dump(outline, f, indent=2)

        # Also save as markdown for easy reading
        with open(os.path.join(output_dir, 'outline.md'), 'w') as f:
            f.write(f"# {outline['title']}\n\n")
            f.write(f"## Book Description\n\n{outline['description']}\n\n")
            f.write("## Chapters\n\n")

            for chapter in outline['chapters']:
                f.write(f"### Chapter {chapter['number']}: {chapter['title']}\n\n")
                f.write(f"{chapter['description']}\n\n")

    def save_chapter(self, content, book_dir, chapter_number):
         """Saves chapter content to a markdown file."""
         chapters_dir = os.path.join(book_dir, 'chapters')
         os.makedirs(chapters_dir, exist_ok=True)

         filename = f"chapter_{chapter_number:02d}.md"
         with open(os.path.join(chapters_dir, filename), 'w') as f:
             f.write(content)

if __name__ == "__main__":
    # Example usage (for testing purposes)
    load_dotenv()
    api_key = os.getenv('ABACUSAI_API_KEY')
    if not api_key:
        print("Error: ABACUSAI_API_KEY not found in environment variables")
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage: python ebook_generator.py <topic> <audience> [output_directory] [num_chapters]")
        print("Example: python ebook_generator.py 'modern psychology' 'Gen Z readers' psychology_gen_z 8")
        sys.exit(1)

    topic = sys.argv[1]
    audience = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else f"{topic.replace(' ', '_').lower()}"
    num_chapters = int(sys.argv[4]) if len(sys.argv) > 4 else 10

    generator = EbookGenerator(api_key)
    generator.generate_full_book(topic, audience, output_dir, num_chapters)
