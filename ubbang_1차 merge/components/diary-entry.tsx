"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Calendar, Smile, Frown, Meh } from "lucide-react"

interface DiaryEntryType {
  id: string
  date: Date
  title: string
  content: string
  emotion: "happy" | "sad" | "neutral" | "excited" | "anxious"
  imageUrl: string
  summary: string
}

interface DiaryEntryProps {
  entry: DiaryEntryType
  onBack: () => void
}

export default function DiaryEntry({ entry, onBack }: DiaryEntryProps) {
  const getEmotionIcon = (emotion: string) => {
    switch (emotion) {
      case "happy":
      case "excited":
        return <Smile className="w-4 h-4" />
      case "sad":
      case "anxious":
        return <Frown className="w-4 h-4" />
      default:
        return <Meh className="w-4 h-4" />
    }
  }

  const getEmotionColor = (emotion: string) => {
    switch (emotion) {
      case "happy":
        return "bg-green-100 text-green-800"
      case "excited":
        return "bg-yellow-100 text-yellow-800"
      case "sad":
        return "bg-blue-100 text-blue-800"
      case "anxious":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getEmotionLabel = (emotion: string) => {
    switch (emotion) {
      case "happy":
        return "기쁨"
      case "excited":
        return "설렘"
      case "sad":
        return "슬픔"
      case "anxious":
        return "불안"
      default:
        return "평온"
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 p-4">
      <div className="max-w-2xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" onClick={onBack} className="text-gray-600 hover:text-gray-800">
            <ArrowLeft className="w-4 h-4 mr-2" />
            돌아가기
          </Button>
        </div>

        {/* Entry Card */}
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
          <CardContent className="p-0">
            <img
              src={entry.imageUrl || "/placeholder.svg"}
              alt={entry.title}
              className="w-full h-64 object-cover rounded-t-lg"
            />
            <div className="p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-gray-800">{entry.title}</h1>
                <Badge className={`${getEmotionColor(entry.emotion)} border-0`}>
                  {getEmotionIcon(entry.emotion)}
                  <span className="ml-1">{getEmotionLabel(entry.emotion)}</span>
                </Badge>
              </div>

              <div className="flex items-center text-gray-500 text-sm">
                <Calendar className="w-4 h-4 mr-2" />
                {entry.date.toLocaleDateString("ko-KR", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                  weekday: "long",
                })}
              </div>

              <div className="prose prose-gray max-w-none">
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{entry.content}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
