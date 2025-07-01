"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Gift } from "lucide-react"
import CharacterCard from "@/components/character-card"
import CharacterUnlock from "@/components/character-unlock"

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

interface CharacterCollectionProps {
  user: {
    nickname: string
    loginMethod: string
    isAnonymous: boolean
  }
}

export default function CharacterCollection({ user }: CharacterCollectionProps) {
  const [characters, setCharacters] = useState<Character[]>([
    // Sweet Breads
    {
      id: "1",
      name: "소금이",
      description: "버터향 가득 짭짤 소금빵 친구",
      rarity: "common",
      imageUrl: "/images/breads/salt_bread.png",
      unlocked: true,
      unlockedAt: new Date(),
      requiredChats: 1,
      category: "sweet",
    },
    {
      id: "2",
      name: "초코링",
      description: "초콜릿이 가득한 도넛",
      rarity: "common",
      imageUrl: "/images/breads/choco_bread.png",
      unlocked: true,
      unlockedAt: new Date(),
      requiredChats: 3,
      category: "sweet",
    },
    {
      id: "3",
      name: "딸기공주",
      description: "딸기잼이 들어간 특별한 빵",
      rarity: "rare",
      imageUrl: "/images/breads/strawberry_bread.png",
      unlocked: true,
      unlockedAt: new Date(),
      requiredChats: 5,
      category: "sweet",
    },
    {
      id: "4",
      name: "허니베어",
      description: "꿀이 듬뿍 들어간 곰 모양 빵",
      rarity: "rare",
      imageUrl: "/images/breads/bear_bread.png",
      unlocked: true,
      requiredChats: 10,
      category: "sweet",
    },
    {
      id: "5",
      name: "바닐라킹",
      description: "바닐라 크림의 왕",
      rarity: "epic",
      imageUrl: "/images/breads/vanilla_bread.png",
      unlocked: true,
      requiredChats: 15,
      category: "sweet",
    },

    // Savory Breads
    {
      id: "6",
      name: "치즈볼",
      description: "치즈가 쭉쭉 늘어나는 빵",
      rarity: "common",
      imageUrl: "/images/breads/cheese_bread.png",
      unlocked: false,
      requiredChats: 2,
      category: "savory",
    },
    {
      id: "7",
      name: "피자왕",
      description: "피자 토핑이 올라간 빵",
      rarity: "rare",
      imageUrl: "/images/breads/pizza_bread.png",
      unlocked: false,
      requiredChats: 7,
      category: "savory",
    },
    {
      id: "8",
      name: "햄버거",
      description: "햄과 야채가 들어간 든든한 빵",
      rarity: "rare",
      imageUrl: "/images/breads/hamburger_bread.png",
      unlocked: true,
      requiredChats: 12,
      category: "savory",
    },

    // Special Breads
    {
      id: "9",
      name: "무지개빵",
      description: "7가지 색깔의 신비한 빵",
      rarity: "legendary",
      imageUrl: "/images/breads/rainbow_bread.png",
      unlocked: true,
      requiredChats: 30,
      category: "special",
    },
    {
      id: "10",
      name: "별빛빵",
      description: "별처럼 반짝이는 마법의 빵",
      rarity: "legendary",
      imageUrl: "/images/breads/star2_bread.png",
      unlocked: true,
      requiredChats: 50,
      category: "special",
    },
  ])

  const [selectedCategory, setSelectedCategory] = useState<"all" | "sweet" | "savory" | "special">("all")
  const [showUnlock, setShowUnlock] = useState<Character | null>(null)
  const [userStats, setUserStats] = useState({
    totalChats: 8,
    unlockedCount: 3,
    totalCharacters: 40,
  })

  const filteredCharacters = characters.filter(
    (char) => selectedCategory === "all" || char.category === selectedCategory,
  )

  const getRarityColor = (rarity: string) => {
    switch (rarity) {
      case "common":
        return "bg-gray-100 text-gray-800"
      case "rare":
        return "bg-blue-100 text-blue-800"
      case "epic":
        return "bg-purple-100 text-purple-800"
      case "legendary":
        return "bg-yellow-100 text-yellow-800"
      default:
        return "bg-gray-100 text-gray-800"
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

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case "sweet":
        return "달콤한 빵"
      case "savory":
        return "고소한 빵"
      case "special":
        return "특별한 빵"
      default:
        return "전체 빵"
    }
  }

  const handleCharacterClick = (character: Character) => {
    if (!character.unlocked && userStats.totalChats >= character.requiredChats) {
      // Unlock character
      const updatedCharacters = characters.map((char) =>
        char.id === character.id ? { ...char, unlocked: true, unlockedAt: new Date() } : char,
      )
      setCharacters(updatedCharacters)
      setUserStats((prev) => ({ ...prev, unlockedCount: prev.unlockedCount + 1 }))
      setShowUnlock(character)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 p-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="w-16 h-16 bg-gradient-to-br from-yellow-200 to-orange-200 rounded-full flex items-center justify-center shadow-lg">
              <Gift className="w-8 h-8 text-yellow-600" />
            </div>
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">나 보러와!</h1>
            <p className="text-gray-600">너 내가 얼마나 멋진지 모르지?!</p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-amber-600">{userStats.unlockedCount}</div>
              <div className="text-sm text-gray-600">내 모습이야!</div>
              <Progress value={(userStats.unlockedCount / userStats.totalCharacters) * 100} className="mt-2" />
            </CardContent>
          </Card>
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-orange-600">{userStats.totalChats}</div>
              <div className="text-sm text-gray-600">나랑 이만큼 놀았어!</div>
            </CardContent>
          </Card>
          <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {Math.round((userStats.unlockedCount / userStats.totalCharacters) * 100)}%
              </div>
              <div className="text-sm text-gray-600">아직 넌 날 다 몰라~</div>
            </CardContent>
          </Card>
        </div>

        {/* Category Filter */}
        <Card className="bg-white/80 backdrop-blur-sm border-0 shadow-lg">
          <CardContent className="p-4">
            <div className="flex flex-wrap gap-2">
              {["all", "sweet", "savory", "special"].map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  size="sm"
                  onClick={() => setSelectedCategory(category as any)}
                  className={
                    selectedCategory === category
                      ? "bg-gradient-to-r from-amber-400 to-orange-400 text-white"
                      : "border-gray-300"
                  }
                >
                  {getCategoryLabel(category)}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Character Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {filteredCharacters.map((character) => (
            <CharacterCard
              key={character.id}
              character={character}
              userChats={userStats.totalChats}
              onClick={() => handleCharacterClick(character)}
            />
          ))}
        </div>

        {/* Unlock Modal */}
        {showUnlock && <CharacterUnlock character={showUnlock} onClose={() => setShowUnlock(null)} />}
      </div>
    </div>
  )
}
