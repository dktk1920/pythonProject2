"use client"

import { useUser } from "@/hooks/useUser"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Heart, Mail, Lock, MessageCircle } from "lucide-react"
import { useState , useEffect} from "react"

console.log("💡 LoginScreen 렌더링 확인!")

interface LoginScreenProps {
  onLogin: (userData: {
      name: string;
      nickname: string;
      userId: string;
      loginMethod: string;
      isAnonymous: boolean;
      gender: string;
      age: number;
      mode: string}) => void
  onNavigate: (screen: string) => void
}


export default function LoginScreen({ onLogin, onNavigate }: LoginScreenProps) {

const [userId, setUserId] = useState("");
const [password, setPassword] = useState("");
const [errors, setErrors] = useState<{ userId?: string; password?: string }>({})

useEffect(() => {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  console.log("✅ 환경변수:", baseUrl);
}, []);

const handleEmailLogin = async () => {
  const newErrors: typeof errors = {}

  if (!userId.trim()) newErrors.userId = "아이디를 입력해주세요"
  if (!password.trim()) newErrors.password = "비밀번호를 입력해주세요"

  if (Object.keys(newErrors).length > 0) {
    setErrors(newErrors)
    return
  }

  setErrors({})  // 에러 초기화

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, password }),
      })

      if (!response.ok) {
        const error = await response.json()
        alert(error.detail || "로그인 실패")
        return
      }

      const data = await response.json()

      console.log("🔐 로그인 응답 데이터:", data)

      localStorage.setItem("user", JSON.stringify({
        name: data.name,
        userId: data.userId,
        loginMethod: data.loginMethod,
        isAnonymous: data.isAnonymous,
      }))

      // 이후 로그인 상태 처리
      onLogin(data)

    } catch (err) {
      alert("서버 연결 오류")
      console.error(err)
    }

}

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Logo/Header */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-gradient-to-br from-amber-200 to-orange-200 rounded-full flex items-center justify-center shadow-lg">
              <Heart className="w-8 h-8 text-amber-600" />
            </div>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">WhaT's your Feeling</h1>
            <p className="text-gray-600">오늘 하루는 어땠어?</p>
          </div>
        </div>

        {/* Login Card */}
        <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-xl text-gray-800">로그인</CardTitle>
            <CardDescription className="text-gray-600">오늘 하루도 수고했어</CardDescription>
          </CardHeader>

          <CardContent className="space-y-4">
            {/* ID Form */}
            <div className="space-y-3">
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    type="text"
                    name="userId"
                    value={userId}
                    onChange={(e) => setUserId(e.target.value)}
                    autoComplete="off"
                    placeholder="아이디"
                    className={`pl-10 h-12 border-gray-200 focus:border-amber-300 focus:ring-amber-200 rounded-xl ${
                      errors.userId ? "border-red-300" : ""
                    }`}
                  />
                  {errors.userId && <p className="text-xs text-red-600 mt-1">{errors.userId}</p>}
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    type="password"
                    name="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                    placeholder="비밀번호"
                    className={`pl-10 h-12 border-gray-200 focus:border-amber-300 focus:ring-amber-200 rounded-xl ${
                      errors.password ? "border-red-300" : ""
                    }`}
                  />
                  {errors.password && <p className="text-xs text-red-600 mt-1">{errors.password}</p>}
                </div>
              </div>
              <Button
                onClick={handleEmailLogin}
                className="w-full h-12 bg-gradient-to-r from-amber-400 to-orange-400 hover:from-amber-500 hover:to-orange-500 text-white rounded-xl shadow-lg transition-all duration-200"
              >
                로그인
              </Button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-white text-gray-500">또는</span>
              </div>
            </div>

            {/* SNS Login */}
            <Button
              onClick={() => onNavigate("sns-auth")}
              className="w-full h-12 bg-yellow-400 hover:bg-yellow-500 text-yellow-900 rounded-xl shadow-lg transition-all duration-200"
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              카카오톡으로 로그인
            </Button>
                        <Button
              onClick={() => onNavigate("sns-auth")}
              className="w-full h-12 bg-green-400 hover:bg-green-500 text-green-900 rounded-xl shadow-lg transition-all duration-200"
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              네이버로 로그인
            </Button>
                        <Button
              onClick={() => onNavigate("sns-auth")}
              className="w-full h-12 bg-blue-400 hover:bg-blue-500 text-white-900 rounded-xl shadow-lg transition-all duration-200"
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              구글로 로그인
            </Button>

            {/* Anonymous Login */}
            <Button
              onClick={() => onNavigate("anonymous-onboarding")}
              variant="outline"
              className="w-full h-12 border-gray-200 text-gray-600 hover:bg-gray-50 rounded-xl transition-all duration-200"
            >
              비회원으로 시작하기
            </Button>

            {/* Sign Up Link */}
            <div className="text-center pt-2">
              <button
                onClick={() => onNavigate("signup")}
                className="text-sm text-blue-600 hover:text-blue-700 transition-colors"
              >
                계정이 없으신가요? 회원가입
              </button>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500">
          <p>오늘 하루도 고생한 너를 위한 너만의 작은 쉼터</p>
        </div>
      </div>
    </div>
  )
}
