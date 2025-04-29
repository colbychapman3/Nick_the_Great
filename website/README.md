# The Indoor Eden Co. Website

This website was created as a platform for The Indoor Eden Co. brand to provide plant care information while monetizing through affiliate links. This README provides guidance on how to use and extend this website.

## Website Structure

- **index.html**: Homepage with main brand messaging and featured content
- **about.html**: Information about the brand, mission, and values
- **affiliate-disclosure.html**: Legal disclosure about affiliate relationships
- **contact.html**: Contact form and brand contact information
- **blog/best-plants-for-beginners.html**: Sample blog post with affiliate links
- **css/style.css**: Main stylesheet with brand colors and styling

## Next Steps

### Image Assets

The website currently references several image files that need to be created or sourced:

1. **Logo**: Create a simple text-based or leaf icon logo using the brand color palette
2. **Plant Images**: Source royalty-free plant images from sites like:
   - [Unsplash](https://unsplash.com/s/photos/houseplants)
   - [Pexels](https://www.pexels.com/search/houseplants/)
   - [Pixabay](https://pixabay.com/images/search/houseplants/)
3. **Product Images**: Source product images for affiliate products (ensure you have rights to use these)

Once sourced, place these images in the `/website/img/` directory.

### Implementation Options

#### Option 1: Use as-is (Static HTML)

You can use this website as-is by uploading the files to any web hosting service that supports static HTML websites. This is the simplest option to get started.

#### Option 2: WordPress Implementation

Follow the steps in `brand/implementation_plan.md` to create a WordPress site based on this design:

1. Create a WordPress.com account
2. Choose a clean, minimal theme
3. Apply the brand colors and styling
4. Create the core pages (Home, About, etc.)
5. Set up the blog structure

#### Option 3: Build on This Foundation

This website provides a starting point that you can expand by:
- Adding more blog posts following the template in `blog/best-plants-for-beginners.html`
- Creating category pages for different plant types
- Adding a product recommendations page organized by category

## Affiliate Program Setup

Before you can monetize this website, you'll need to:

1. **Apply to Amazon Associates**: Visit [Amazon Associates](https://affiliate-program.amazon.com/) to register
2. **Set up tracking**: Implement proper tracking for your affiliate links
3. **Consider additional programs**: Look into plant-specific affiliate programs (e.g., plant shops, garden supply retailers)

## Legal Considerations

Ensure that:
1. The affiliate disclosure is linked from all pages with affiliate links
2. You have a privacy policy (you can create one using WordPress tools or online generators)
3. You comply with data protection regulations if collecting user information

## Tracking and Analytics

Consider setting up:
1. **Google Analytics**: To track visitor behavior
2. **Affiliate link tracking**: To identify which content drives conversions

## Tracking Affiliate Income

The affiliate-income-tracker MCP server has been configured and can be used to track and analyze your affiliate income once you start earning. It provides tools for monitoring earnings, analyzing performance, and generating optimization suggestions.

## Getting Help

For questions or assistance with this website, you can:
- Refer to the brand guidelines in `brand/brand_identity.md`
- Review the implementation plan in `brand/implementation_plan.md`
