import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: "WhaT's your Feeling",
  description: 'Created by Ubbang',
  generator: 'team Ubbang',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
