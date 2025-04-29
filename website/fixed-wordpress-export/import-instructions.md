# WordPress Import Instructions

This package contains a complete WordPress export file (`wordpress-export.xml`) that includes all pages, blog posts, and categories from The Indoor Eden Co. website. Follow these steps to import this content into your WordPress site.

## Prerequisites

- A working WordPress installation (either self-hosted or WordPress.com)
- Administrator access to your WordPress site

## Import Steps

1. **Log in to your WordPress Admin Dashboard**
   - Navigate to yourdomain.com/wp-admin and log in with your credentials

2. **Install the WordPress Importer Plugin (if not already installed)**
   - Go to **Tools** → **Import**
   - Find **WordPress** in the list and click **Install Now**
   - After installation completes, click **Run Importer**

3. **Upload the WordPress Export File**
   - Click **Choose File** and select the `wordpress-export.xml` file from this package
   - Click **Upload file and import**

4. **Map Authors**
   - You'll be prompted to map the authors from the import file to users on your site
   - You can create a new user for "The Indoor Eden Team" or map it to an existing user
   - Click **Submit** when you're done mapping authors

5. **Import Attachments**
   - Check the box next to **Download and import file attachments**
   - This will attempt to import the images referenced in the content
   - Click **Submit** to begin the import process

6. **Wait for Import to Complete**
   - The import process may take several minutes depending on the size of the file
   - You'll see a "All done" message when the import is complete

## After Import

1. **Check Your Content**
   - Navigate to **Pages** and **Posts** in your WordPress admin to verify all content was imported correctly
   - Some formatting may need adjustment depending on your theme

2. **Upload Images**
   - If images were not imported correctly, you'll need to upload them manually to your Media Library
   - All necessary images are included in the `wordpress-export/img/` directory

3. **Update Menu Structure**
   - Go to **Appearance** → **Menus** to set up your navigation menu
   - Add the imported pages to your main navigation

4. **Apply Custom CSS**
   - Go to **Appearance** → **Customize** → **Additional CSS**
   - Copy the contents of `wordpress-export/css/style.css` into this section for custom styling

## Troubleshooting

- **Import Fails**: Try splitting the XML file into smaller parts if the import fails due to file size limitations
- **Missing Images**: If images don't import correctly, check your server's file permissions and upload them manually
- **Formatting Issues**: Content formatting may vary depending on your WordPress theme - you may need to adjust some pages manually

## Additional Resources

- [WordPress Importer Documentation](https://wordpress.org/support/article/importing-content/#wordpress)
- [WordPress.org Support](https://wordpress.org/support/)
