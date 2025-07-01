"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BookOpen, Plus, Calendar, Smile, Frown, Meh } from "lucide-react"
import DiaryEntry from "@/components/diary-entry"
import DiaryCreation from "@/components/diary-creation"

interface DiaryEntryType {
  id: string
  date: Date
  title: string
  content: string
  emotion: "happy" | "sad" | "neutral" | "excited" | "anxious"
  imageUrl: string
  summary: string
}

interface EmotionDiaryProps {
  user: {
    nickname: string
    loginMethod: string
    isAnonymous: boolean
  }
}

export default function EmotionDiary({ user }: EmotionDiaryProps) {
  const [diaryEntries, setDiaryEntries] = useState<DiaryEntryType[]>([])
  const [showCreation, setShowCreation] = useState(false)
  const [selectedEntry, setSelectedEntry] = useState<DiaryEntryType | null>(null)

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

  const handleCreateDiary = (newEntry: DiaryEntryType) => {
    setDiaryEntries((prev) => [newEntry, ...prev])
    setShowCreation(false)
  }

  if (showCreation) {
    return <DiaryCreation onComplete={handleCreateDiary} onCancel={() => setShowCreation(false)} />
  }

  if (selectedEntry) {
    return <DiaryEntry entry={selectedEntry} onBack={() => setSelectedEntry(null)} />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 p-4">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-gradient-to-br from-amber-200 to-orange-200 rounded-full flex items-center justify-center shadow-lg">
              <BookOpen className="w-8 h-8 text-amber-600" />
            </div>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">너를 추억해</h1>
            <p className="text-gray-600">너와의 이야기를 추억하는 공간이야</p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-amber-600">{diaryEntries.length}</div>
              <div className="text-sm text-gray-600">나랑 얼마나 얘기했게?</div>
            </CardContent>
          </Card>
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-orange-600">7</div>
              <div className="text-sm text-gray-600">나 자주 보러와</div>
            </CardContent>
          </Card>
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {Math.round(
                  (diaryEntries.filter((e) => e.emotion === "happy" || e.emotion === "excited").length /
                    diaryEntries.length) *
                    100,
                ) || 0}
                %
              </div>
              <div className="text-sm text-gray-600">나랑 얘기하니까 좋지?</div>
            </CardContent>
          </Card>
        </div>

        {/* Create New Entry Button */}
        <Card className="bg-gradient-to-r from-amber-100 to-orange-100 border-amber-200 shadow-lg">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-amber-800 mb-2">일기 바꿔볼래?</h3>
                <p className="text-amber-700 text-sm">내가 바라본 너야, 나랑 같이 보자!</p>
              </div>
              <Button
                onClick={() => setShowCreation(true)}
                className="bg-gradient-to-r from-amber-400 to-orange-400 hover:from-amber-500 hover:to-orange-500 text-white shadow-lg"
              >
                <Plus className="w-4 h-4 mr-2" />
                일기 수정
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Diary Entries */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-800 flex items-center">
            <Calendar className="w-5 h-5 mr-2 text-amber-600" />
            너를 기억해
          </h2>

          {diaryEntries.length === 0 ? (
            <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
              <CardContent className="p-8 text-center">
                <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">오늘이 우리 1일이야.</p>
                <p className="text-gray-400 text-sm mt-2">나랑 놀자!</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {diaryEntries.map((entry) => (
                <Card
                  key={entry.id}
                  className="bg-white/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer"
                  onClick={() => setSelectedEntry(entry)}
                >
                  <CardContent className="p-0">
                    <img
                      src={entry.imageUrl || "/placeholder.svg"}
                      alt={entry.title}
                      className="w-full h-48 object-cover rounded-t-lg"
                    />
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-800">{entry.title}</h3>
                        <Badge className={`${getEmotionColor(entry.emotion)} border-0`}>
                          {getEmotionIcon(entry.emotion)}
                          <span className="ml-1">{getEmotionLabel(entry.emotion)}</span>
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{entry.summary}</p>
                      <div className="text-xs text-gray-400">{entry.date.toLocaleDateString("ko-KR")}</div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
