# AI-Generated Ebook Project

This directory contains tools and content for generating ebooks using AI as part of the Autonomous Money Generation Framework (AMGF).

## Setup

1. Install required packages:
   ```
   python -m pip install abacusai python-dotenv
   ```

2. Create a `.env` file with your AbacusAI API key:
   ```
   ABACUSAI_API_KEY=your_api_key_here
   ```

## Usage

### Generating a Book

Use the `generate_book.py` script to create a complete ebook:

```
python generate_book.py <topic> <audience> [output_directory] [num_chapters]
```

Example:
```
python generate_book.py "modern psychology" "Gen Z readers" psychology_gen_z 8
```

This will:
1. Generate a book outline with title, description, and chapter summaries
2. Create content for each chapter
3. Save everything to the specified output directory

### Output Structure

The script creates the following files:
- `outline.json` - JSON file containing the book structure
- `outline.md` - Markdown version of the outline for easy reading
- `chapters/chapter_XX.md` - Individual chapter content files

## Workflow

1. **Research Phase**: Identify profitable niche topics with high demand but low competition
2. **Generation Phase**: Use the script to generate book content
3. **Editing Phase**: Review and refine the AI-generated content
4. **Publishing Phase**: Format the content for publishing platforms (Amazon KDP, Gumroad, etc.)
5. **Marketing Phase**: Create promotional materials and list on platforms

## Next Steps

After generating the initial content:
1. Edit and refine the content for quality and accuracy
2. Create a professional cover using Canva
3. Format the book for different platforms
4. Set up accounts on publishing platforms
5. Publish and begin marketing

## Resources

- [Amazon KDP](https://kdp.amazon.com)
- [Gumroad](https://gumroad.com)
- [Canva](https://canva.com) - For cover design