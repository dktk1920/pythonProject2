import { useState, useEffect } from "react"

let globalUser: any = null
let setGlobalUser: ((val: any) => void) | null = null

export function useUser() {
  const [user, _setUser] = useState<any>(null)

  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    if (storedUser) {
      const parsed = JSON.parse(storedUser)
      globalUser = parsed
      _setUser(parsed)
    }

    // ✅ useEffect 안에서 setGlobalUser 설정
    setGlobalUser = _setUser
  }, [])

  return {
    user,
    setUser: (val: any) => {
      globalUser = val
      localStorage.setItem("user", JSON.stringify(val))
      setGlobalUser?.(val)
    }
  }
}
