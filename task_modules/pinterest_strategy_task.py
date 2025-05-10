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

class PinterestStrategyTask:
    """
    Task module for creating and executing Pinterest marketing strategies.
    This class is designed to be called by the Agent Core Service.
    """
    
    def __init__(self):
        """
        Initialize the PinterestStrategyTask.
        The API key is loaded from environment variables when execute() is called.
        """
        self.api_key = None
        self.client = None
        logger.info("PinterestStrategyTask initialized")
    
    def execute(self, parameters):
        """
        Execute the Pinterest strategy task with the provided parameters.
        
        Args:
            parameters (google.protobuf.Struct): Parameters for the Pinterest strategy task.
                Expected fields:
                - niche: The specific niche for the Pinterest strategy
                - target_audience: The target audience for the Pinterest content
                - business_goal: The primary business goal (traffic, sales, brand awareness)
                - num_pins: (Optional) Number of pin ideas to generate
                - board_structure: (Optional) Suggested board structure
        
        Returns:
            dict: A dictionary containing the task result with the following fields:
                - status: "completed" or "failed"
                - result: (If completed) Information about the generated Pinterest strategy
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
            
            logger.info(f"Executing Pinterest strategy task with parameters: {params}")
            
            # Validate required parameters
            if 'niche' not in params:
                return {"status": "failed", "message": "Missing required parameter: niche"}
            if 'target_audience' not in params:
                return {"status": "failed", "message": "Missing required parameter: target_audience"}
            if 'business_goal' not in params:
                return {"status": "failed", "message": "Missing required parameter: business_goal"}
            
            # Get parameters
            niche = params['niche']
            target_audience = params['target_audience']
            business_goal = params['business_goal']
            num_pins = int(params.get('num_pins', 10))  # Default to 10 pin ideas
            board_structure = params.get('board_structure', 'recommended')
            
            # Get API key from environment
            self.api_key = os.getenv('ABACUSAI_API_KEY')
            if not self.api_key:
                return {"status": "failed", "message": "ABACUSAI_API_KEY not found in environment variables"}
            
            # Initialize AbacusAI client
            self.client = ApiClient(self.api_key)
            
            # Generate Pinterest strategy
            pinterest_strategy = self._generate_pinterest_strategy(niche, target_audience, business_goal, board_structure)
            if not pinterest_strategy:
                return {"status": "failed", "message": "Failed to generate Pinterest strategy"}
            
            # Generate pin ideas
            pin_ideas = self._generate_pin_ideas(niche, target_audience, business_goal, num_pins)
            if not pin_ideas:
                return {"status": "failed", "message": "Failed to generate pin ideas"}
            
            # Generate pin descriptions
            pin_descriptions = self._generate_pin_descriptions(niche, target_audience, pin_ideas[:3])
            
            # Create temporary directory for output
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save strategy
                strategy_file = os.path.join(temp_dir, "pinterest_strategy.json")
                with open(strategy_file, 'w') as f:
                    json.dump(pinterest_strategy, f, indent=2)
                
                # Save pin ideas
                pins_file = os.path.join(temp_dir, "pin_ideas.json")
                with open(pins_file, 'w') as f:
                    json.dump(pin_ideas, f, indent=2)
                
                # Save pin descriptions
                if pin_descriptions:
                    descriptions_file = os.path.join(temp_dir, "pin_descriptions.json")
                    with open(descriptions_file, 'w') as f:
                        json.dump(pin_descriptions, f, indent=2)
                
                # Return success result
                return {
                    "status": "completed",
                    "result": {
                        "niche": niche,
                        "target_audience": target_audience,
                        "business_goal": business_goal,
                        "pinterest_strategy": pinterest_strategy,
                        "pin_ideas": pin_ideas,
                        "pin_descriptions": pin_descriptions
                    }
                }
                
        except Exception as e:
            logger.error(f"Error executing Pinterest strategy task: {e}", exc_info=True)
            return {"status": "failed", "message": f"Error executing Pinterest strategy task: {str(e)}"}
    
    def _generate_pinterest_strategy(self, niche, target_audience, business_goal, board_structure):
        """
        Generate a comprehensive Pinterest marketing strategy.
        
        Returns:
            dict: Pinterest strategy structure or None on error
        """
        try:
            prompt = f"""
            Create a detailed Pinterest marketing strategy for a business in the {niche} niche, targeting {target_audience}, with the primary goal of {business_goal}.
            
            Format the response as a JSON object with the following structure:
            {{
                "profile_optimization": {{
                    "business_name": "Suggested business name for Pinterest",
                    "username": "Suggested username",
                    "bio": "Suggested bio text",
                    "profile_image_description": "Description of ideal profile image",
                    "keywords": ["keyword1", "keyword2"]
                }},
                "board_strategy": {{
                    "recommended_boards": [
                        {{
                            "name": "Board name",
                            "description": "Board description",
                            "keywords": ["keyword1", "keyword2"],
                            "content_focus": "What type of content to pin to this board"
                        }}
                    ],
                    "board_cover_strategy": "Strategy for board covers",
                    "organization_tips": "Tips for organizing boards"
                }},
                "content_strategy": {{
                    "pin_types": [
                        {{
                            "type": "Pin type (idea pin, standard pin, etc.)",
                            "best_uses": "When to use this pin type",
                            "creation_tips": "Tips for creating this type of pin"
                        }}
                    ],
                    "optimal_posting_frequency": "Recommended posting frequency",
                    "seasonal_strategy": "How to adapt for seasonal trends",
                    "content_themes": ["theme1", "theme2"]
                }},
                "growth_tactics": {{
                    "follower_growth": [
                        "Tactic 1",
                        "Tactic 2"
                    ],
                    "engagement_strategies": [
                        "Strategy 1",
                        "Strategy 2"
                    ],
                    "collaboration_opportunities": [
                        "Opportunity 1",
                        "Opportunity 2"
                    ]
                }},
                "analytics_focus": {{
                    "key_metrics": [
                        "Metric 1",
                        "Metric 2"
                    ],
                    "success_indicators": [
                        "Indicator 1",
                        "Indicator 2"
                    ],
                    "optimization_approach": "How to use analytics to optimize strategy"
                }},
                "monetization_path": {{
                    "traffic_strategy": "How to drive traffic from Pinterest",
                    "conversion_optimization": "Tips for converting Pinterest traffic",
                    "product_integration": "How to integrate products naturally"
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
            pinterest_strategy = json.loads(response.generations[0].text)
            logger.info(f"Generated Pinterest strategy for {niche} niche")
            return pinterest_strategy
            
        except Exception as e:
            logger.error(f"Error generating Pinterest strategy: {e}", exc_info=True)
            return None
    
    def _generate_pin_ideas(self, niche, target_audience, business_goal, num_pins):
        """
        Generate pin ideas for the Pinterest strategy.
        
        Returns:
            list: List of pin ideas or None on error
        """
        try:
            prompt = f"""
            Generate {num_pins} Pinterest pin ideas for a business in the {niche} niche, targeting {target_audience}, with the primary goal of {business_goal}.
            
            Format the response as a JSON array with the following structure for each pin:
            [
                {{
                    "title": "Pin title/headline",
                    "type": "Pin type (standard, idea pin, video, etc.)",
                    "description": "Brief description of the pin content",
                    "visual_elements": ["Element 1", "Element 2"],
                    "call_to_action": "Suggested call to action",
                    "target_board": "Which board this would fit on",
                    "target_keywords": ["keyword1", "keyword2"],
                    "seasonal_relevance": "When this pin would be most relevant"
                }}
            ]
            """
            
            response = self.client.text_generation(
                prompt=prompt,
                max_tokens=3000,
                temperature=0.7,
                model="claude-3-opus-20240229"
            )
            
            # Parse the JSON response
            pin_ideas = json.loads(response.generations[0].text)
            logger.info(f"Generated {len(pin_ideas)} pin ideas for {niche} niche")
            return pin_ideas
            
        except Exception as e:
            logger.error(f"Error generating pin ideas: {e}", exc_info=True)
            return None
    
    def _generate_pin_descriptions(self, niche, target_audience, pin_ideas):
        """
        Generate optimized descriptions for the provided pin ideas.
        
        Returns:
            list: List of pin descriptions or None on error
        """
        try:
            if not pin_ideas or len(pin_ideas) == 0:
                return []
            
            # Convert pin ideas to string representation
            pin_ideas_str = json.dumps(pin_ideas, indent=2)
            
            prompt = f"""
            Create optimized Pinterest pin descriptions for these pin ideas in the {niche} niche, targeting {target_audience}:
            
            {pin_ideas_str}
            
            For each pin, provide:
            1. An SEO-optimized description (up to 500 characters)
            2. A set of relevant hashtags (5-10)
            3. A compelling call-to-action
            
            Format the response as a JSON array with the following structure for each pin:
            [
                {{
                    "pin_title": "Title from the original pin idea",
                    "optimized_description": "SEO-optimized description text",
                    "hashtags": ["#hashtag1", "#hashtag2"],
                    "call_to_action": "Compelling call-to-action text"
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
            pin_descriptions = json.loads(response.generations[0].text)
            logger.info(f"Generated optimized descriptions for {len(pin_descriptions)} pins")
            return pin_descriptions
            
        except Exception as e:
            logger.error(f"Error generating pin descriptions: {e}", exc_info=True)
            return None
