// 로컬시 필요
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  devIndicators: false,
  async rewrites() {
    return [
      {
        source: "/api/:path*", // 프론트에서 /api/xxx로 요청하면
        destination: "http://localhost:8000/:path*", // 백엔드로 전달됨
      },
    ];
  },
};

export default nextConfig;
