llmimport os
import sys
import json
from dotenv import load_dotenv
from abacusai import ApiClient

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('ABACUSAI_API_KEY')
if not api_key:
    print("Error: ABACUSAI_API_KEY not found in environment variables")
    sys.exit(1)

# Initialize AbacusAI client
client = ApiClient(api_key)

def generate_book_outline(topic, audience, num_chapters=10):
    """
    Generate a book outline with chapter titles and brief descriptions
    
    Args:
        topic (str): The main topic of the book
        audience (str): The target audience for the book
        num_chapters (int): Number of chapters to generate
        
    Returns:
        dict: Book outline with title, description, and chapters
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
        response = client.text_generation(
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7,
            model="claude-3-opus-20240229"
        )
        
        # Parse the JSON response
        outline = json.loads(response.generations[0].text)
        return outline
    except Exception as e:
        print(f"Error generating book outline: {e}")
        return None

def generate_chapter_content(book_title, chapter_info, audience):
    """
    Generate content for a specific chapter
    
    Args:
        book_title (str): The title of the book
        chapter_info (dict): Chapter information including number, title, and description
        audience (str): The target audience for the book
        
    Returns:
        str: Generated chapter content
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
        response = client.text_generation(
            prompt=prompt,
            max_tokens=4000,
            temperature=0.7,
            model="claude-3-opus-20240229"
        )
        
        return response.generations[0].text
    except Exception as e:
        print(f"Error generating chapter content: {e}")
        return None

def save_outline(outline, output_dir):
    """Save the book outline to a JSON file"""
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

def save_chapter(content, book_dir, chapter_number):
    """Save chapter content to a markdown file"""
    chapters_dir = os.path.join(book_dir, 'chapters')
    os.makedirs(chapters_dir, exist_ok=True)
    
    filename = f"chapter_{chapter_number:02d}.md"
    with open(os.path.join(chapters_dir, filename), 'w') as f:
        f.write(content)

def generate_full_book(topic, audience, output_dir, num_chapters=10):
    """Generate a complete book including outline and all chapters"""
    print(f"Generating book outline for '{topic}' targeted at {audience}...")
    outline = generate_book_outline(topic, audience, num_chapters)
    
    if not outline:
        print("Failed to generate book outline. Exiting.")
        return
    
    print(f"Book outline generated: {outline['title']}")
    save_outline(outline, output_dir)
    
    for chapter in outline['chapters']:
        print(f"Generating Chapter {chapter['number']}: {chapter['title']}...")
        content = generate_chapter_content(outline['title'], chapter, audience)
        
        if content:
            save_chapter(content, output_dir, chapter['number'])
            print(f"Chapter {chapter['number']} completed and saved.")
        else:
            print(f"Failed to generate content for Chapter {chapter['number']}.")
    
    print(f"Book generation complete. Files saved to {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_book.py <topic> <audience> [output_directory] [num_chapters]")
        print("Example: python generate_book.py 'modern psychology' 'Gen Z readers' psychology_gen_z 8")
        sys.exit(1)
    
    topic = sys.argv[1]
    audience = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else f"{topic.replace(' ', '_').lower()}"
    num_chapters = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    
    generate_full_book(topic, audience, output_dir, num_chapters)