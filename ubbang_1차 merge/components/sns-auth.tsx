"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, MessageCircle, Smartphone, Shield, CheckCircle } from "lucide-react"

interface SnsAuthProps {
  onComplete: (userData: { nickname: string; loginMethod: string; isAnonymous: boolean }) => void
  onBack: () => void
}

export default function SnsAuth({ onComplete, onBack }: SnsAuthProps) {
  const [step, setStep] = useState<"select" | "authenticating" | "complete">("select")
  const [selectedProvider, setSelectedProvider] = useState<string>("")

  const handleSnsLogin = (provider: string) => {
    setSelectedProvider(provider)
    setStep("authenticating")

    // SNS 인증 시뮬레이션
    setTimeout(() => {
      setStep("complete")
      setTimeout(() => {
        onComplete({
          nickname: `${provider} 사용자`,
          loginMethod: `${provider} 계정`,
          isAnonymous: false,
        })
      }, 1500)
    }, 2000)
  }

  const snsProviders = [
    {
      id: "kakao",
      name: "카카오톡",
      icon: MessageCircle,
      color: "bg-yellow-400 hover:bg-yellow-500 text-yellow-900",
      description: "카카오 계정으로 간편하게 로그인",
    },
    {
      id: "naver",
      name: "네이버",
      icon: Smartphone,
      color: "bg-green-500 hover:bg-green-600 text-white",
      description: "네이버 계정으로 간편하게 로그인",
    },
    {
      id: "google",
      name: "구글",
      icon: Shield,
      color: "bg-blue-500 hover:bg-blue-600 text-white",
      description: "구글 계정으로 간편하게 로그인",
    },
  ]

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50">
      <div className="w-full max-w-md space-y-6">
        {/* Header */}
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" onClick={onBack} className="text-gray-600 hover:text-gray-800">
            <ArrowLeft className="w-4 h-4 mr-2" />
            돌아가기
          </Button>
        </div>

        {step === "select" && (
          <>
            <div className="text-center space-y-4">
              <div className="flex justify-center">
                <div className="w-16 h-16 bg-gradient-to-br from-amber-200 to-orange-200 rounded-full flex items-center justify-center shadow-lg">
                  <Shield className="w-8 h-8 text-amber-600" />
                </div>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800 mb-2">소셜 로그인</h1>
                <p className="text-gray-600">간편하고 안전하게 로그인하세요</p>
              </div>
            </div>

            <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader className="text-center pb-4">
                <CardTitle className="text-lg text-gray-800">로그인 방법 선택</CardTitle>
                <CardDescription className="text-gray-600">소셜 계정으로 빠르고 안전하게 시작하세요</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {snsProviders.map((provider) => {
                  const IconComponent = provider.icon
                  return (
                    <Button
                      key={provider.id}
                      onClick={() => handleSnsLogin(provider.name)}
                      className={`w-full h-14 ${provider.color} rounded-xl shadow-lg transition-all duration-200 flex items-center justify-start px-6`}
                    >
                      <IconComponent className="w-6 h-6 mr-4" />
                      <div className="text-left">
                        <div className="font-semibold">{provider.name}으로 로그인</div>
                        <div className="text-xs opacity-80">{provider.description}</div>
                      </div>
                    </Button>
                  )
                })}

                {/* Benefits */}
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 mt-6">
                  <h4 className="text-sm font-medium text-blue-800 mb-2">소셜 로그인의 장점</h4>
                  <ul className="text-xs text-blue-700 space-y-1">
                    <li>• 별도 회원가입 불필요</li>
                    <li>• 안전한 OAuth 인증</li>
                    <li>• 빠른 로그인 과정</li>
                    <li>• 개인정보 최소 수집</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </>
        )}

        {step === "authenticating" && (
          <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-amber-200 to-orange-200 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                <Shield className="w-8 h-8 text-amber-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">{selectedProvider} 인증 중</h3>
              <p className="text-gray-600">안전한 인증을 진행하고 있습니다...</p>
            </CardContent>
          </Card>
        )}

        {step === "complete" && (
          <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">인증 완료!</h3>
              <p className="text-gray-600">{selectedProvider} 계정으로 로그인되었습니다</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
