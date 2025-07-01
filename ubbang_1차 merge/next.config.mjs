// next.config.mjs
export default {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  experimental: {
    allowedDevOrigins: ["http://192.168.0.39:3000"], // 본인 IP로 교체
  },
  devIndicators: false,
};
