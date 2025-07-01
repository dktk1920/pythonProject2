"use client"

import type React from "react"
import { useUser } from "@/hooks/useUser"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Send, Clock } from "lucide-react"
import MessageBubble from "@/components/message-bubble"
import SessionSummary from "@/components/session-summary"

interface Message {
  id: string
  content: string
  sender: "user" | "ai"
  timestamp: Date
}

interface ChatInterfaceProps {
  // props로 받는 user의 이름을 initialUserInfo로 변경
  initialUserInfo: {
    name: string
    loginMethod: string
    isAnonymous: boolean
  }
}

export default function ChatInterface({ initialUserInfo }: ChatInterfaceProps) {
  const { user } = useUser()
  const userName = user?.name || initialUserInfo?.name || "사용자";
  const ws = useRef<WebSocket | null>(null)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: `안녕하세요 ${userName || initialUserInfo.name}님! 저는 우빵이입니다. 오늘 하루는 어떠셨나요? 편안하게 이야기해 주세요.`,
      sender: "ai",
      timestamp: new Date(),
    },
  ])
  const [inputMessage, setInputMessage] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [isUserTyping, setIsUserTyping] = useState(false)
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const mode = user.mode || "banmal"
    const gender = user.gender || "female"

    ws.current = new WebSocket(`ws://localhost:8000/ws?mode=${mode}&gender=${gender}`)

    ws.current.onmessage = (event) => {
      const aiMessage: Message = {
        id: Date.now().toString(),
        content: event.data,
        sender: "ai",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
      setIsTyping(false)
    }

    ws.current.onopen = () => console.log("WebSocket 연결됨")
    ws.current.onerror = () => console.log("WebSocket 오류 발생")
    ws.current.onclose = () => console.log("WebSocket 종료됨")

    return () => {
      ws.current?.close()
    }
  }, [user.mode, user.gender])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputMessage(e.target.value)
    setIsUserTyping(true)
    if (typingTimeoutRef.current) clearTimeout(typingTimeoutRef.current)
    typingTimeoutRef.current = setTimeout(() => {
      setIsUserTyping(false)
    }, 1000)
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isUserTyping) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      sender: "user",
      timestamp: new Date(),
    }
    ws.current?.send(inputMessage)
    setMessages((prev) => [...prev, userMessage])
    setInputMessage("")
    setIsTyping(true)

    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200 shadow-sm">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center space-x-3">
            <img
              src="/images/bread2.png"
              alt="서포터 프로필"
              className="w-10 h-10 rounded-full border-2 border-amber-200 shadow-sm"
            />
            <div>
              <h1 className="text-lg font-semibold text-gray-800">우빵이</h1>
              <p className="text-sm text-gray-500">WhaT's your Feeling</p>
            </div>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Clock className="w-4 h-4" />
            <span>온라인</span>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <SessionSummary />

        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isTyping && (
          <div className="flex justify-start items-end space-x-3">
            <img
              src="/images/bread2.png"
              alt="서포터"
              className="w-8 h-8 rounded-full border border-amber-200 shadow-sm"
            />
            <div className="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100 max-w-xs">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-amber-400 rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-amber-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-amber-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
                <span className="text-xs text-gray-500 ml-2">작성 중...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white/80 backdrop-blur-sm border-t border-gray-200 p-4">
        <div className="flex items-end space-x-3">
          <div className="flex-1">
            <Input
              value={inputMessage}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              placeholder="너의 이야기를 들려줘"
              className="min-h-[48px] resize-none border-gray-200 focus:border-amber-300 focus:ring-amber-200 rounded-2xl px-4 py-3"
              disabled={isTyping}
            />
          </div>
          <Button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isTyping || isUserTyping}
            className="h-12 w-12 rounded-full bg-gradient-to-r from-amber-400 to-orange-400 hover:from-amber-500 hover:to-orange-500 shadow-lg transition-all duration-200"
          >
            <Send className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>
  )
}
