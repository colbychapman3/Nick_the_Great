/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Configure images
  images: {
    domains: ['api.dicebear.com'],
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: 'https://nick-the-great-api.onrender.com',
  },
  
  // API routes proxying
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://nick-the-great-api.onrender.com/api/:path*',
      },
    ];
  },
  
  // Enhance page discovery
  pageExtensions: ['tsx', 'ts', 'jsx', 'js', 'md', 'mdx'],
};

export default nextConfig;
