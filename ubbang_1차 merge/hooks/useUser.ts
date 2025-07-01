// hooks/useUser.ts
import { useState } from "react"

let globalUser: any = {
  name: "",
  nickname: "",
  loginMethod: "",
  isAnonymous: true,
  gender: "female",
  mode: "banmal"
}

let setGlobalUser: ((val: any) => void) | null = null

export function useUser() {
  const [user, _setUser] = useState(globalUser)

  setGlobalUser = _setUser

  return {
    user,
    setUser: (val: any) => {
      globalUser = val
      setGlobalUser?.(val)
    }
  }
}
