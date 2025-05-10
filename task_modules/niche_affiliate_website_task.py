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

class NicheAffiliateWebsiteTask:
    """
    Task module for creating and managing niche affiliate websites.
    This class is designed to be called by the Agent Core Service.
    """
    
    def __init__(self):
        """
        Initialize the NicheAffiliateWebsiteTask.
        The API key is loaded from environment variables when execute() is called.
        """
        self.api_key = None
        self.client = None
        logger.info("NicheAffiliateWebsiteTask initialized")
    
    def execute(self, parameters):
        """
        Execute the niche affiliate website task with the provided parameters.
        
        Args:
            parameters (google.protobuf.Struct): Parameters for the niche affiliate website task.
                Expected fields:
                - niche: The specific niche for the affiliate website
                - target_audience: The target audience for the website
                - affiliate_programs: (Optional) List of affiliate programs to use
                - num_articles: (Optional) Number of initial articles to generate
                - monetization_strategy: (Optional) Primary monetization strategy
        
        Returns:
            dict: A dictionary containing the task result with the following fields:
                - status: "completed" or "failed"
                - result: (If completed) Information about the generated website plan
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
            
            logger.info(f"Executing niche affiliate website task with parameters: {params}")
            
            # Validate required parameters
            if 'niche' not in params:
                return {"status": "failed", "message": "Missing required parameter: niche"}
            if 'target_audience' not in params:
                return {"status": "failed", "message": "Missing required parameter: target_audience"}
            
            # Get parameters
            niche = params['niche']
            target_audience = params['target_audience']
            affiliate_programs = params.get('affiliate_programs', [])
            num_articles = int(params.get('num_articles', 5))  # Default to 5 articles
            monetization_strategy = params.get('monetization_strategy', 'affiliate links')
            
            # Get API key from environment
            self.api_key = os.getenv('ABACUSAI_API_KEY')
            if not self.api_key:
                return {"status": "failed", "message": "ABACUSAI_API_KEY not found in environment variables"}
            
            # Initialize AbacusAI client
            self.client = ApiClient(self.api_key)
            
            # Generate website plan
            website_plan = self._generate_website_plan(niche, target_audience, affiliate_programs, monetization_strategy)
            if not website_plan:
                return {"status": "failed", "message": "Failed to generate website plan"}
            
            # Generate article ideas
            article_ideas = self._generate_article_ideas(niche, target_audience, num_articles)
            if not article_ideas:
                return {"status": "failed", "message": "Failed to generate article ideas"}
            
            # Generate sample article
            sample_article = None
            if article_ideas and len(article_ideas) > 0:
                sample_article = self._generate_sample_article(niche, target_audience, article_ideas[0])
            
            # Create temporary directory for output
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save website plan
                plan_file = os.path.join(temp_dir, "website_plan.json")
                with open(plan_file, 'w') as f:
                    json.dump(website_plan, f, indent=2)
                
                # Save article ideas
                articles_file = os.path.join(temp_dir, "article_ideas.json")
                with open(articles_file, 'w') as f:
                    json.dump(article_ideas, f, indent=2)
                
                # Save sample article if generated
                if sample_article:
                    article_file = os.path.join(temp_dir, "sample_article.md")
                    with open(article_file, 'w') as f:
                        f.write(sample_article)
                
                # Return success result
                result = {
                    "niche": niche,
                    "target_audience": target_audience,
                    "website_plan": website_plan,
                    "article_ideas": article_ideas,
                }
                
                if sample_article:
                    result["sample_article"] = {
                        "title": article_ideas[0]["title"],
                        "content_preview": sample_article[:200] + "..." if len(sample_article) > 200 else sample_article
                    }
                
                return {
                    "status": "completed",
                    "result": result
                }
                
        except Exception as e:
            logger.error(f"Error executing niche affiliate website task: {e}", exc_info=True)
            return {"status": "failed", "message": f"Error executing niche affiliate website task: {str(e)}"}
    
    def _generate_website_plan(self, niche, target_audience, affiliate_programs, monetization_strategy):
        """
        Generate a comprehensive plan for the niche affiliate website.
        
        Returns:
            dict: Website plan structure or None on error
        """
        try:
            # Prepare affiliate programs string
            programs_str = ", ".join(affiliate_programs) if affiliate_programs else "to be determined based on niche research"
            
            prompt = f"""
            Create a detailed plan for a niche affiliate website in the {niche} niche, targeted at {target_audience}.
            The primary monetization strategy will be {monetization_strategy}, using these affiliate programs: {programs_str}.
            
            Format the response as a JSON object with the following structure:
            {{
                "website_name": "Suggested domain name for the website",
                "tagline": "Catchy tagline for the website",
                "unique_selling_proposition": "What makes this website unique and valuable",
                "site_structure": {{
                    "homepage": "Description of homepage content and layout",
                    "main_categories": [
                        "Category 1",
                        "Category 2"
                    ],
                    "key_pages": [
                        {{
                            "title": "Page title",
                            "purpose": "Purpose of this page",
                            "content_outline": "Brief outline of the content"
                        }}
                    ]
                }},
                "monetization": {{
                    "primary_strategy": "{monetization_strategy}",
                    "affiliate_programs": [
                        {{
                            "name": "Program name",
                            "fit": "Why this program fits the niche",
                            "commission_structure": "Typical commission structure"
                        }}
                    ],
                    "secondary_strategies": [
                        {{
                            "strategy": "Secondary monetization strategy",
                            "implementation": "How to implement this strategy"
                        }}
                    ]
                }},
                "seo_strategy": {{
                    "primary_keywords": [
                        "Keyword 1",
                        "Keyword 2"
                    ],
                    "long_tail_keywords": [
                        "Long tail keyword 1",
                        "Long tail keyword 2"
                    ],
                    "content_strategy": "Overview of content strategy for SEO"
                }},
                "marketing_plan": {{
                    "target_platforms": [
                        "Platform 1",
                        "Platform 2"
                    ],
                    "content_promotion": "How to promote the website content",
                    "audience_building": "Strategies for building an audience"
                }}
            }}
            """
            
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=3000,
                temperature=0.7,
                model="claude-3-opus-20240229"
            )
            
            # Parse the JSON response
            website_plan = json.loads(response.generations[0].text)
            logger.info(f"Generated website plan for {niche} niche")
            return website_plan
            
        except Exception as e:
            logger.error(f"Error generating website plan: {e}", exc_info=True)
            return None
    
    def _generate_article_ideas(self, niche, target_audience, num_articles):
        """
        Generate article ideas for the niche affiliate website.
        
        Returns:
            list: List of article ideas or None on error
        """
        try:
            prompt = f"""
            Generate {num_articles} article ideas for a niche affiliate website in the {niche} niche, targeted at {target_audience}.
            Each article should have potential for affiliate product integration and SEO value.
            
            Format the response as a JSON array with the following structure for each article:
            [
                {{
                    "title": "Compelling article title",
                    "type": "Article type (how-to, review, comparison, etc.)",
                    "description": "Brief description of the article content",
                    "target_keywords": ["keyword1", "keyword2"],
                    "affiliate_opportunities": ["Product category 1", "Product category 2"],
                    "estimated_word_count": 1500
                }}
            ]
            """
            
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7,
                model="claude-3-opus-20240229"
            )
            
            # Parse the JSON response
            article_ideas = json.loads(response.generations[0].text)
            logger.info(f"Generated {len(article_ideas)} article ideas for {niche} niche")
            return article_ideas
            
        except Exception as e:
            logger.error(f"Error generating article ideas: {e}", exc_info=True)
            return None
    
    def _generate_sample_article(self, niche, target_audience, article_idea):
        """
        Generate a sample article based on the provided idea.
        
        Returns:
            str: Generated article content or None on error
        """
        try:
            # Extract article details
            title = article_idea.get("title", "Untitled Article")
            article_type = article_idea.get("type", "informational")
            description = article_idea.get("description", "")
            target_keywords = article_idea.get("target_keywords", [])
            affiliate_opportunities = article_idea.get("affiliate_opportunities", [])
            word_count = article_idea.get("estimated_word_count", 1500)
            
            # Prepare keywords and affiliate opportunities strings
            keywords_str = ", ".join(target_keywords) if target_keywords else "no specific keywords"
            affiliate_str = ", ".join(affiliate_opportunities) if affiliate_opportunities else "relevant products in the niche"
            
            prompt = f"""
            Write a complete {article_type} article titled "{title}" for a niche affiliate website in the {niche} niche, targeted at {target_audience}.
            
            Article description: {description}
            
            The article should:
            - Be approximately {word_count} words
            - Target these keywords: {keywords_str}
            - Include natural opportunities to mention or link to these affiliate products/categories: {affiliate_str}
            - Be well-structured with clear headings and subheadings
            - Provide genuine value to the reader while naturally incorporating affiliate opportunities
            - Be formatted in Markdown
            
            Please provide the complete, ready-to-publish article.
            """
            
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=4000,
                temperature=0.7,
                model="claude-3-opus-20240229"
            )
            
            content = response.generations[0].text
            logger.info(f"Generated sample article: {title}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating sample article: {e}", exc_info=True)
            return None
