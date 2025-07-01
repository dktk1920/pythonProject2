"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Lock, Star } from "lucide-react"

interface Character {
  id: string
  name: string
  description: string
  rarity: "common" | "rare" | "epic" | "legendary"
  imageUrl: string
  unlocked: boolean
  unlockedAt?: Date
  requiredChats: number
  category: "sweet" | "savory" | "special"
}

interface CharacterCardProps {
  character: Character
  userChats: number
  onClick: () => void
}

export default function CharacterCard({ character, userChats, onClick }: CharacterCardProps) {
  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case "common":
        return "bg-gray-100 text-gray-800 border-gray-300"
      case "rare":
        return "bg-blue-100 text-blue-800 border-blue-300"
      case "epic":
        return "bg-purple-100 text-purple-800 border-purple-300"
      case "legendary":
        return "bg-yellow-100 text-yellow-800 border-yellow-300"
      default:
        return "bg-gray-100 text-gray-800 border-gray-300"
    }
  }

  const getRarityLabel = (rarity: string) => {
    switch (rarity) {
      case "common":
        return "일반"
      case "rare":
        return "레어"
      case "epic":
        return "에픽"
      case "legendary":
        return "전설"
      default:
        return "일반"
    }
  }

  const canUnlock = !character.unlocked && userChats >= character.requiredChats

  return (
    <Card
      className={`bg-white/80 backdrop-blur-sm border-0 shadow-lg transition-all duration-200 cursor-pointer ${
        canUnlock
          ? "hover:shadow-xl hover:scale-105 ring-2 ring-yellow-300"
          : character.unlocked
            ? "hover:shadow-xl"
            : "opacity-60"
      }`}
      onClick={onClick}
    >
      <CardContent className="p-4 text-center space-y-3">
        <div className="relative">
          <div
            className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl ${
              character.unlocked ? "bg-gradient-to-br from-amber-100 to-orange-100" : "bg-gray-100"
            }`}
          >
            {character.unlocked ? (
              <img
                src={character.imageUrl || "/placeholder.svg"}
                alt={character.name}
                className="w-12 h-12 rounded-full"
              />
            ) : (
              <Lock className="w-6 h-6 text-gray-400" />
            )}
          </div>
          {canUnlock && (
            <div className="absolute -top-1 -right-1 w-6 h-6 bg-yellow-400 rounded-full flex items-center justify-center animate-pulse">
              <Star className="w-3 h-3 text-white" />
            </div>
          )}
        </div>

        <div>
          <h3 className={`font-semibold text-sm ${character.unlocked ? "text-gray-800" : "text-gray-400"}`}>
            {character.unlocked ? character.name : "???"}
          </h3>
          <p className={`text-xs mt-1 ${character.unlocked ? "text-gray-600" : "text-gray-400"}`}>
            {character.unlocked ? character.description : `${character.requiredChats}회 대화 필요`}
          </p>
        </div>

        <Badge className={`text-xs ${getRarityColor(character.rarity)}`}>{getRarityLabel(character.rarity)}</Badge>

        {canUnlock && <div className="text-xs text-yellow-600 font-medium animate-pulse">획득 가능!</div>}
      </CardContent>
    </Card>
  )
}
