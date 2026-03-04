import { useState } from "react"
import { fetchRandom, createPunishment } from "./api"
import type { Punishment } from "./api"

function App() {
  const [category, setCategory] = useState("")
  const [result, setResult] = useState<Punishment | null>(null)
  const [newContent, setNewContent] = useState("")
  const [newCategory, setNewCategory] = useState("light")

  const handleRandom = async () => {
    try {
      const data = await fetchRandom(category || undefined)
      setResult(data)
    } catch (e) {
      alert("取得失敗")
    }
  }

  const handleCreate = async () => {
    if (!newContent) return
    await createPunishment(newContent, newCategory)
    setNewContent("")
    alert("追加成功！")
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>🎲 Punish Roulette</h1>

      <div>
        <select onChange={(e) => setCategory(e.target.value)}>
          <option value="">すべて</option>
          <option value="light">軽い</option>
          <option value="embarrassing">恥ずかしい</option>
          <option value="physical">運動系</option>
        </select>

        <button onClick={handleRandom}>罰ゲームを引く</button>
      </div>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h2>🔥 結果</h2>
          <p>{result.content}</p>
        </div>
      )}

      <hr style={{ margin: 30 }} />

      <h2>➕ 罰ゲーム追加</h2>
      <input
        value={newContent}
        onChange={(e) => setNewContent(e.target.value)}
        placeholder="内容"
      />

      <select
        value={newCategory}
        onChange={(e) => setNewCategory(e.target.value)}
      >
        <option value="light">軽い</option>
        <option value="embarrassing">恥ずかしい</option>
        <option value="physical">運動系</option>
      </select>

      <button onClick={handleCreate}>追加</button>
    </div>
  )
}

export default App