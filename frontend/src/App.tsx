import { useState } from "react"
import { fetchRandom, createPunishment } from "./api"
import type { Punishment } from "./api"

function App() {
  const [category, setCategory] = useState("")
  const [result, setResult] = useState<Punishment | null>(null)
  const [newContent, setNewContent] = useState("")
  const [newCategory, setNewCategory] = useState("light")
  const [loading, setLoading] = useState(false)

  const handleRandom = async () => {
    try {
      setLoading(true)
      const data = await fetchRandom(category || undefined)
      setResult(data)
    } catch {
      alert("取得失敗")
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async () => {
    if (!newContent) return
    await createPunishment(newContent, newCategory)
    setNewContent("")
    alert("追加成功！")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md space-y-6">

        <h1 className="text-3xl font-bold text-center text-gray-800">
          🎲 Punish Roulette
        </h1>

        {/* 罰ゲーム取得 */}
        <div className="space-y-3">
          <select
            className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="">すべて</option>
            <option value="light">軽い</option>
            <option value="embarrassing">恥ずかしい</option>
            <option value="physical">運動系</option>
          </select>

          <button
            onClick={handleRandom}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition duration-200"
          >
            {loading ? "抽選中..." : "罰ゲームを引く"}
          </button>
        </div>

        {/* 結果表示 */}
        {loading && (
          <div className="text-center py-6">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent mx-auto"></div>
            <p className="mt-3 text-gray-600">ルーレット回転中...</p>
          </div>
        )}

        {result && !loading && (
          <div className="bg-gray-100 rounded-xl p-4 shadow-inner animate-bounce">
            <h2 className="text-lg font-semibold mb-2 text-gray-700">
              🔥 結果
            </h2>
            <p className="text-gray-800 text-lg font-medium">
              {result.content}
            </p>
          </div>
        )}

        <hr />

        {/* 追加フォーム */}
        <div className="space-y-3">
          <h2 className="text-xl font-semibold text-gray-700">
            ➕ 罰ゲーム追加
          </h2>

          <input
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
            placeholder="内容"
            className="w-full border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-pink-400"
          />

          <select
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
            className="w-full border rounded-lg p-2"
          >
            <option value="light">軽い</option>
            <option value="embarrassing">恥ずかしい</option>
            <option value="physical">運動系</option>
          </select>

          <button
            onClick={handleCreate}
            className="w-full bg-pink-500 hover:bg-pink-600 text-white font-semibold py-2 rounded-xl transition"
          >
            追加する
          </button>
        </div>
      </div>
    </div>
  )
}

export default App