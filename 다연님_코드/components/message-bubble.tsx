import { format } from "date-fns"
import { ko } from "date-fns/locale"

interface Message {
  id: string
  content: string
  sender: "user" | "ai"
  timestamp: Date
}

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.sender === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} items-end space-x-2`}>
      {!isUser && (
        <img
          src="/images/bread2.png"
          alt="서포터"
          className="w-8 h-8 rounded-full border border-amber-200 shadow-sm mb-6"
        />
      )}
      <div className={`max-w-xs lg:max-w-md ${isUser ? "order-2" : "order-1"}`}>
        <div
          className={`px-4 py-3 rounded-2xl shadow-sm ${
            isUser
              ? "bg-gradient-to-r from-amber-400 to-orange-400 text-white"
              : "bg-white border border-gray-100 text-gray-800"
          } ${isUser ? "rounded-br-md" : "rounded-bl-md"}`}
        >
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
        </div>
        <div className={`mt-1 px-2 ${isUser ? "text-right" : "text-left"}`}>
          <span className="text-xs text-gray-400">{format(message.timestamp, "HH:mm", { locale: ko })}</span>
        </div>
      </div>
    </div>
  )
}
