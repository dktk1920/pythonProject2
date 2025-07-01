"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ChevronDown, ChevronUp, FileText, X } from "lucide-react"

export default function SessionSummary() {
  const [isExpanded, setIsExpanded] = useState(false)
  const [isVisible, setIsVisible] = useState(true)

  if (!isVisible) return null

  return (
    <Card className="bg-gradient-to-r from-amber-50 to-orange-50 border-amber-200 shadow-sm">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-2 mb-2">
            <FileText className="w-4 h-4 text-amber-600" />
            <h3 className="text-sm font-medium text-amber-800">오늘 하루도 수고했어</h3>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsVisible(false)}
            className="h-6 w-6 p-0 text-amber-600 hover:text-amber-700 hover:bg-amber-100"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="text-sm text-amber-700 leading-relaxed">
          <p>
            오늘 서울엔 비가 왔어, 너네 동네는 어땠어?
            {isExpanded && (
              <span>
                {" "}
                여기는 비가 갑자기 쏟아져서 신발도 옷도 젖어서 너무 불쾌했어😂😂
                너네 동네는 어때? 장마라 너무 짜증나💢💢
              </span>
            )}
          </p>
        </div>

        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-2 h-6 text-xs text-amber-600 hover:text-amber-700 hover:bg-amber-100 p-0"
        >
          {isExpanded ? (
            <>
              <ChevronUp className="w-3 h-3 mr-1" />
              접기
            </>
          ) : (
            <>
              <ChevronDown className="w-3 h-3 mr-1" />
              더보기
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  )
}
