/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['api.dicebear.com'],
  },
  env: {
    NEXT_PUBLIC_API_URL: 'https://nick-the-great-api.onrender.com',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://nick-the-great-api.onrender.com/api/:path*',
      },
    ];
  },
};

export default nextConfig;
