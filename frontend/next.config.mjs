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
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'https://nick-the-great.onrender.com'}/api/:path*`,
      },
    ];
  },
  
  // Enhance page discovery
  pageExtensions: ['tsx', 'ts', 'jsx', 'js', 'md', 'mdx'],
};

export default nextConfig;
