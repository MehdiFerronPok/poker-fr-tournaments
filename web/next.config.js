/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    appDir: true
  },
  i18n: {
    locales: ['fr'],
    defaultLocale: 'fr'
  },
  images: {
    unoptimized: true
  }
};

module.exports = nextConfig;