const BASE_URL = import.meta.env.VITE_API_URL

export type Punishment = {
  id: number
  content: string
  category: string
  createdAt: string
}

export async function fetchRandom(category?: string): Promise<Punishment> {
  const url = category
    ? `${BASE_URL}/punishments/random?category=${category}`
    : `${BASE_URL}/punishments/random`

  const res = await fetch(url)
  if (!res.ok) throw new Error("Failed to fetch")

  return res.json()
}

export async function createPunishment(content: string, category: string) {
  const res = await fetch(`${BASE_URL}/punishments`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content, category }),
  })

  if (!res.ok) throw new Error("Failed to create")

  return res.json()
}

export const likePunishment = async (id: number) => {
  const res = await fetch(`${BASE_URL}/punishments/${id}/like`, {
    method: "POST",
  })
  return res.json()
}

export const fetchPopular = async () => {
  const res = await fetch(`${BASE_URL}/punishments/popular`)
  return res.json()
}