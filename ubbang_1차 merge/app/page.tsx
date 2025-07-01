"use client"

import { useState } from "react"
import ChatInterface from "@/components/chat-interface"
import LoginScreen from "@/components/login-screen"
import ProfileSettings from "@/components/profile-settings"
import EmotionDiary from "@/components/emotion-diary"
import CharacterCollection from "@/components/character-collection"
import AnonymousOnboarding from "@/components/anonymous-onboarding"
import SnsAuth from "@/components/sns-auth"
import Signup from "@/components/signup"
import { Button } from "@/components/ui/button"

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<
    "login" | "chat" | "profile" | "diary" | "collection" | "anonymous-onboarding" | "sns-auth" | "signup"
  >("login")

    const [user, setUser] = useState<{
      name: string
      userId: string
      loginMethod: string
      isAnonymous: boolean
      gender?: string
      birthDate?: string
      email?: string
    } | null>(null)

    const handleLogin = (userData: {
      name: string
      userId: string
      loginMethod: string
      isAnonymous: boolean
      gender?: string
      birthDate?: string
      email?: string
    }) => {
      setUser(userData)
      setCurrentScreen("chat")
    }
  const handleLogout = () => {
    setUser(null)
    setCurrentScreen("login")
  }

  const handleNavigate = (screen: string) => {
    setCurrentScreen(screen as any)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50">
      {/* Navigation for demo purposes */}
      {user && (
        <div className="fixed top-4 right-4 z-50 flex gap-2">
          <Button
            variant={currentScreen === "chat" ? "default" : "outline"}
            size="sm"
            onClick={() => setCurrentScreen("chat")}
            className="bg-amber-100 hover:bg-amber-200 text-amber-800 border-amber-200"
          >
            오늘도 고생했어
          </Button>
          <Button
            variant={currentScreen === "diary" ? "default" : "outline"}
            size="sm"
            onClick={() => setCurrentScreen("diary")}
            className="bg-orange-100 hover:bg-orange-200 text-orange-800 border-orange-200"
          >
            너를 추억해
          </Button>
          <Button
            variant={currentScreen === "collection" ? "default" : "outline"}
            size="sm"
            onClick={() => setCurrentScreen("collection")}
            className="bg-yellow-100 hover:bg-yellow-200 text-yellow-800 border-yellow-200"
          >
            나 보러와
          </Button>
          <Button
            variant={currentScreen === "profile" ? "default" : "outline"}
            size="sm"
            onClick={() => setCurrentScreen("profile")}
            className="bg-amber-100 hover:bg-amber-200 text-amber-800 border-amber-200"
          >
            이게 너야
          </Button>
        </div>
      )}

      {/* Login Flow */}
      {currentScreen === "login" && <LoginScreen onLogin={handleLogin} onNavigate={handleNavigate} />}

      {currentScreen === "anonymous-onboarding" && (
        <AnonymousOnboarding onComplete={handleLogin} onBack={() => setCurrentScreen("login")} />
      )}

      {currentScreen === "sns-auth" && <SnsAuth onComplete={handleLogin} onBack={() => setCurrentScreen("login")} />}

      {currentScreen === "signup" && <Signup onComplete={handleLogin} onBack={() => setCurrentScreen("login")} />}

      {/* Main App Screens */}
      {currentScreen === "chat" && user && <ChatInterface user={user} />}

      {currentScreen === "profile" && user && <ProfileSettings user={user} onLogout={handleLogout} />}

      {currentScreen === "diary" && user && <EmotionDiary user={user} />}

      {currentScreen === "collection" && user && <CharacterCollection user={user} />}
    </div>
  )
}
