import os
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

def research_profitable_niches(num_niches=10):
    """
    Research potentially profitable ebook niches with high demand but low competition
    
    Args:
        num_niches (int): Number of niche ideas to generate
        
    Returns:
        list: List of niche ideas with analysis
    """
    prompt = f"""
    Research and identify {num_niches} potentially profitable niche topics for ebooks that have:
    1. High search interest/demand
    2. Low competition (not oversaturated with existing books)
    3. Audience willing to pay for information
    
    For each niche:
    - Provide a specific topic (not too broad)
    - Identify the target audience
    - Explain why this niche has potential (demand factors)
    - Suggest a potential book title
    - Rate the profit potential on a scale of 1-10
    
    Format the response as a JSON array with the following structure:
    [
        {{
            "niche": "Specific niche topic",
            "audience": "Target audience description",
            "demand_factors": "Explanation of why this niche has potential",
            "sample_title": "Potential book title",
            "profit_potential": 8,
            "keywords": ["keyword1", "keyword2", "keyword3"]
        }},
        ...
    ]
    
    Focus on niches where AI-generated content could provide genuine value, and where the information isn't rapidly changing or requiring deep specialized expertise that AI might struggle with.
    """
    
    try:
        response = client.text_generation(
            prompt=prompt,
            max_tokens=3000,
            temperature=0.7,
            model="claude-3-opus-20240229"
        )
        
        # Parse the JSON response
        niches = json.loads(response.generations[0].text)
        return niches
    except Exception as e:
        print(f"Error researching profitable niches: {e}")
        return None

def analyze_competition(niche):
    """
    Analyze competition for a specific niche
    
    Args:
        niche (str): The niche to analyze
        
    Returns:
        dict: Competition analysis
    """
    prompt = f"""
    Perform a detailed competition analysis for ebooks in the niche: "{niche}"
    
    Include:
    1. Estimated number of existing books in this niche
    2. Average pricing of competing books
    3. Quality assessment of existing content (are there gaps?)
    4. Barriers to entry
    5. Unique selling proposition opportunities
    
    Format the response as a JSON object with the following structure:
    {{
        "niche": "{niche}",
        "estimated_books": "Approximate number of competing books",
        "price_range": "Typical price range (e.g., $9.99-$19.99)",
        "content_gaps": "Identified gaps in existing content",
        "barriers_to_entry": "Challenges for new entrants",
        "usp_opportunities": "Potential unique selling propositions",
        "overall_competition": "Low/Medium/High",
        "recommendation": "Go/No-go recommendation with brief explanation"
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
        analysis = json.loads(response.generations[0].text)
        return analysis
    except Exception as e:
        print(f"Error analyzing competition: {e}")
        return None

def save_research(niches, output_file):
    """Save the niche research to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(niches, f, indent=2)
    
    # Also save as markdown for easy reading
    md_file = output_file.replace('.json', '.md')
    with open(md_file, 'w') as f:
        f.write("# Profitable Ebook Niche Research\n\n")
        
        for i, niche in enumerate(niches, 1):
            f.write(f"## {i}. {niche['niche']}\n\n")
            f.write(f"**Target Audience:** {niche['audience']}\n\n")
            f.write(f"**Demand Factors:** {niche['demand_factors']}\n\n")
            f.write(f"**Sample Title:** {niche['sample_title']}\n\n")
            f.write(f"**Profit Potential:** {niche['profit_potential']}/10\n\n")
            f.write(f"**Keywords:** {', '.join(niche['keywords'])}\n\n")
            f.write("---\n\n")

def analyze_and_save_competition(niches, output_dir):
    """Analyze competition for each niche and save results"""
    os.makedirs(output_dir, exist_ok=True)
    
    all_analyses = []
    
    for niche in niches:
        print(f"Analyzing competition for: {niche['niche']}...")
        analysis = analyze_competition(niche['niche'])
        
        if analysis:
            all_analyses.append(analysis)
    
    # Save all analyses to a single file
    with open(os.path.join(output_dir, 'competition_analysis.json'), 'w') as f:
        json.dump(all_analyses, f, indent=2)
    
    # Also save as markdown
    with open(os.path.join(output_dir, 'competition_analysis.md'), 'w') as f:
        f.write("# Ebook Niche Competition Analysis\n\n")
        
        for analysis in all_analyses:
            f.write(f"## {analysis['niche']}\n\n")
            f.write(f"**Estimated Books:** {analysis['estimated_books']}\n\n")
            f.write(f"**Price Range:** {analysis['price_range']}\n\n")
            f.write(f"**Content Gaps:** {analysis['content_gaps']}\n\n")
            f.write(f"**Barriers to Entry:** {analysis['barriers_to_entry']}\n\n")
            f.write(f"**USP Opportunities:** {analysis['usp_opportunities']}\n\n")
            f.write(f"**Overall Competition:** {analysis['overall_competition']}\n\n")
            f.write(f"**Recommendation:** {analysis['recommendation']}\n\n")
            f.write("---\n\n")
    
    return all_analyses

if __name__ == "__main__":
    output_dir = "research"
    os.makedirs(output_dir, exist_ok=True)
    
    num_niches = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    print(f"Researching {num_niches} profitable ebook niches...")
    niches = research_profitable_niches(num_niches)
    
    if niches:
        output_file = os.path.join(output_dir, 'niche_research.json')
        save_research(niches, output_file)
        print(f"Niche research completed and saved to {output_file}")
        
        print("Analyzing competition for each niche...")
        analyses = analyze_and_save_competition(niches, output_dir)
        print(f"Competition analysis completed and saved to {os.path.join(output_dir, 'competition_analysis.json')}")
        
        # Print summary of best opportunities
        print("\nTop Opportunities Based on Analysis:")
        go_recommendations = [a for a in analyses if "go" in a['recommendation'].lower()]
        for i, analysis in enumerate(sorted(go_recommendations, key=lambda x: "high" not in x['overall_competition'].lower()), 1):
            print(f"{i}. {analysis['niche']} - Competition: {analysis['overall_competition']}")
    else:
        print("Failed to research profitable niches.")