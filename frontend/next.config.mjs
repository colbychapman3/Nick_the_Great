/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Configure images
  images: {
    domains: ['api.dicebear.com'],
  },

  // Environment variables are managed in Vercel/deployment platform

  // API routes proxying
  async rewrites() {
    // Get the API URL from environment variables or use a fallback
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
    console.log(`Using API URL for rewrites: ${apiUrl}`);

    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },

  // Enhance page discovery
  pageExtensions: ['tsx', 'ts', 'jsx', 'js', 'md', 'mdx'],
};

export default nextConfig;
