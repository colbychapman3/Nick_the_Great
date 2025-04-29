# The Indoor Eden Co.: Implementation Guide

This guide provides step-by-step instructions for implementing The Indoor Eden Co. website, following the plan we've created.

## Step 1: Create Your WordPress.com Site

1. **Create a WordPress.com account**:
   - Go to [WordPress.com](https://wordpress.com/)
   - Click "Start your website"
   - Sign up with your email address
   - Complete the registration process

2. **Choose the free plan**:
   - When prompted to select a plan, choose "Start with a free site"
   - Skip any upsells for premium features

3. **Secure your domain**:
   - Choose subdomain: `theindooreden.wordpress.com`
   - This gives you a free domain while you're starting out
   - You can upgrade to a custom domain (`theindooreden.co`) later when the site generates revenue

4. **Basic site setup**:
   - **Site Title**: The Indoor Eden Co.
   - **Tagline**: "Cultivating Calm. Growing Joy."
   - Set language to English and timezone to your local time

## Step 2: Theme Selection & Brand Implementation

1. **Choose an appropriate theme**:
   - From your WordPress dashboard, go to Appearance → Themes
   - Look for a clean, minimal theme that supports:
     * Clear typography
     * Good readability
     * Simple navigation
     * Mobile responsiveness
   - Recommended free themes: "Twenty Twenty-One", "Seedlet", or "Hever"

2. **Apply brand colors**:
   - Go to Appearance → Customize → Colors
   - Set primary color to Eden Green (#5E7C60)
   - Set accent/button color to Terracotta Clay (#D9A68A)
   - Set background colors to Soft Sage (#CFE1D0) and Sandstone (#F5F1EB)
   - Set text color to Charcoal (#333333)

3. **Create and upload logo**:
   - Use [Canva](https://www.canva.com/) (free version) to create your logo
   - Create a primary logo:
     * New design with dimensions 200x60 pixels
     * Use Playfair Display or Cormorant Garamond font for "The Indoor Eden Co."
     * Add a minimalist palm leaf icon beside the text
     * Use Eden Green (#5E7C60) for the primary color
   - Create a secondary monogram logo:
     * Simple palm leaf with "IEC" initials for favicon and social icons
     * Square dimensions (32x32 pixels for favicon)
   - Download as PNG with transparent background
   - In WordPress, go to Appearance → Customize → Site Identity
   - Upload your primary logo and favicon

## Step 3: Essential Pages Setup

Create these foundation pages for your site:

1. **Homepage**:
   - Go to Pages → Add New
   - Title: "Welcome to The Indoor Eden Co."
   - Content:
   ```
   # Cultivating Calm. Growing Joy.

   The Indoor Eden Co. helps modern urban dwellers create lush, peaceful sanctuaries through intentional indoor plant care and styling.

   ## Find the Perfect Plants for Your Space

   Whether you're dealing with low light, small spaces, or forgetful watering habits, we'll help you find plants that will thrive in your unique environment.

   [Start Here](#) | [Plant Care Basics](#) | [Shop Guides](#)

   ## Latest Guides

   [placeholder for latest articles, to be updated as you publish content]

   ## Most Popular Resources

   * 10 Best Indoor Plants for Absolute Beginners
   * How to Choose the Right Plant for Your Space
   * Essential Tools Every Plant Parent Needs

   ## Join Our Community

   Sign up for plant care tips, exclusive guides, and updates:
   [Email signup placeholder]
   ```
   - Set as your homepage: Go to Settings → Reading → set "Your homepage displays" to "A static page" and select this page

2. **About Page**:
   - Go to Pages → Add New
   - Title: "About The Indoor Eden Co."
   - Content:
   ```
   # About The Indoor Eden Co.

   The Indoor Eden Co. was created to help modern urban dwellers create lush, peaceful sanctuaries through intentional indoor plant care and styling.

   ## Our Mission

   We believe everyone deserves to experience the joy of living with plants. Our mission is to provide accurate, practical advice that works in real-world conditions, making plant parenthood accessible and rewarding for everyone.

   ## Our Approach

   Unlike many plant websites showing perfect specimens in ideal conditions, we focus on:

   * **Real-world conditions**: Plants in apartments, offices, and small spaces
   * **Practical solutions**: Advice that works with your lifestyle, not against it
   * **Honest recommendations**: Products we truly believe in, not just what's trending
   * **Accessible information**: Clear explanations without confusing jargon

   ## About Our Recommendations

   When we recommend products, we focus on value, quality, and performance - not just price. We personally research all products or rely on extensive community feedback to ensure we're only suggesting items that truly work.

   Some links on our site are affiliate links, which means we may earn a commission if you purchase through them. This helps support our work and allows us to continue providing free plant care information. We only recommend products we believe in and would use ourselves.

   ## Connect With Us

   Have questions or suggestions? We'd love to hear from you!

   Email: contact@theindooreden.co
   ```

3. **Start Here Guide**:
   - Go to Pages → Add New
   - Title: "Start Here: Indoor Plant Basics for Beginners"
   - Create an outline based on the "Start Here" section from your content calendar
   - Add placeholder text that you'll expand later

4. **Affiliate Disclosure Page**:
   - Go to Pages → Add New
   - Title: "Affiliate Disclosure"
   - Content:
   ```
   # Affiliate Disclosure

   This page contains affiliate links. This means if you click on a link and purchase a product, we may receive a small commission at no additional cost to you.

   The Indoor Eden Co. is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. We also participate in affiliate programs with other sites.

   We only recommend products we genuinely believe in and that we have researched carefully. Our opinions are not influenced by our affiliate relationships.

   This affiliate program participation helps us cover the costs of running this website and continue to provide free, valuable content about houseplants and their care.

   If you have any questions about this, please contact us at contact@theindooreden.co.
   ```

5. **Privacy Policy Page**:
   - Go to Pages → Add New
   - Title: "Privacy Policy"
   - Use WordPress's built-in privacy policy template as a starting point
   - Customize it for your specific site needs

## Step 4: Navigation Setup

1. **Create main navigation menu**:
   - Go to Appearance → Menus
   - Create a new menu named "Main Navigation"
   - Add these pages:
     * Home
     * Plant Care
     * Find Your Plant
     * Troubleshooting
     * Shop Guides
     * About
   - Note: For now, some of these will be placeholder links. You'll create these category pages as you develop content
   - Set this menu as your "Primary Menu"

2. **Create footer menu**:
   - Create another menu named "Footer Navigation"
   - Add pages:
     * About
     * Contact
     * Privacy Policy
     * Affiliate Disclosure
   - Set this menu as your "Footer Menu"

## Step 5: Category Structure

1. **Set up main categories**:
   - Go to Posts → Categories
   - Create these categories:
     * Plant Care Basics
     * Plant Types
     * Plant Problems
     * Product Guides
     * Spaces & Styling
     * Plant Projects

2. **Create key subcategories**:
   - Under each main category, create relevant subcategories from your content plan
   - For example, under "Plant Types":
     * Beginner-Friendly
     * Low Light Heroes
     * Air Purifiers
     * Pet-Safe Options

## Step 6: First Content Creation

1. **Publish your first article**:
   - Start with "10 Best Indoor Plants for Absolute Beginners"
   - Use the sample article format as a guide for structure
   - Apply proper formatting: headings, bullet points, tables
   - Include relevant affiliate links (at minimum Amazon links)
   - Add free images from sources like Unsplash or Pexels
   - Assign appropriate categories and tags

2. **Create a second foundation article**:
   - "How to Choose the Right Plant for Your Space"
   - This serves as a fundamental resource you can link to from other articles
   - Focus on providing value first, with minimal affiliate links

## Step 7: Amazon Associates Application

1. **Apply to Amazon Associates**:
   - Go to [Amazon Associates](https://affiliate-program.amazon.com/)
   - Sign up with your Amazon account
   - Complete application form:
     * Website URL: theindooreden.wordpress.com
     * Content description: Indoor plant care guides and product recommendations
     * Traffic generation: SEO, Pinterest, content strategy
   - Amazon requires at least some content on your site before approval
   - If initially rejected, you can reapply after adding more content

## Step 8: Analytics Setup

1. **Set up Google Analytics**:
   - Create a Google Analytics account if you don't have one
   - Set up a property for your website
   - On WordPress.com free plan, you'll need to use the "Site Stats" feature
   - Note that more advanced analytics integration requires a paid plan

## Step 9: Content Schedule Implementation

1. **Create content production schedule**:
   - Set up a Google Sheet to track your content pipeline
   - Schedule specific days for research, writing, and publishing
   - Follow the 3-month content calendar from your plan
   - Start with 2-3 posts per week

2. **Content production process**:
   - Research keywords for each planned article
   - Create detailed outlines before writing
   - Find relevant affiliate products to feature
   - Source free images from Unsplash, Pexels, or Pixabay
   - Format articles consistently following your sample template

## Step 10: First Week Content Schedule

Here's what to publish in your first week:

1. **Day 1**: 10 Best Indoor Plants for Absolute Beginners
2. **Day 3**: How to Choose the Right Plant for Your Space
3. **Day 5**: Essential Plant Care Tools for Beginners (with affiliate links)

## Long-Term Next Steps

After implementing the foundation:

1. **Consistent publishing**: Follow your content calendar to build up site content
2. **Affiliate expansion**: Once Amazon Associates is approved, apply to plant-specific programs
3. **Social promotion**: Create Pinterest account and start creating pins for your content
4. **Email collection**: Add a simple sign-up form for a plant care newsletter
5. **Website upgrade**: When revenue begins, consider upgrading to the WordPress Personal plan to remove WordPress.com branding
