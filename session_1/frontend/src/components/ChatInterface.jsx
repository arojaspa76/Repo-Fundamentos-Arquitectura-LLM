/**
 * ChatInterface.jsx
 * =================
 * Interfaz de chat que conecta con el backend FastAPI / Ollama.
 * Demuestra conceptos de: system prompt, temperatura, tokens usados,
 * y latencia de inferencia local vs cloud.
 */

import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

const MODELS = ['llama3.2', 'llama3.1', 'mistral', 'phi3', 'gemma2']

const SYSTEM_PROMPTS = {
  default:  'Eres un asistente experto en LLMs y arquitecturas de IA. Responde siempre en español de forma clara y educativa.',
  concise:  'Responde siempre en español. Sé muy conciso: máximo 3 oraciones.',
  teacher:  'Eres un profesor universitario de IA. Explica los conceptos con analogías simples y ejemplos del mundo real. Responde en español.',
  formal:   'Eres un consultor senior de IA para empresas. Responde en español con un tono profesional y orientado a soluciones empresariales.',
}

export default function ChatInterface() {
  const [messages, setMessages]       = useState([])
  const [input, setInput]             = useState('')
  const [model, setModel]             = useState('llama3.2')
  const [temperature, setTemperature] = useState(0.7)
  const [systemKey, setSystemKey]     = useState('default')
  const [loading, setLoading]         = useState(false)
  const [stats, setStats]             = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const userMsg = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: userMsg }])
    setLoading(true)
    setStats(null)

    try {
      const res = await axios.post(`${API_URL}/chat`, {
        model,
        message: userMsg,
        system_prompt: SYSTEM_PROMPTS[systemKey],
        temperature,
        max_tokens: 512,
      })
      const data = res.data
      setMessages(prev => [...prev, { role: 'assistant', content: data.message }])
      setStats({
        tokens: data.tokens_used,
        prompt: data.prompt_tokens,
        completion: data.completion_tokens,
        duration: data.duration_ms,
      })
    } catch (err) {
      const detail = err.response?.data?.detail
      const msg = typeof detail === 'object'
        ? `❌ ${detail.error}\n💡 ${detail.solution}`
        : `❌ ${detail || 'Error al conectar con el servidor'}`
      setMessages(prev => [...prev, { role: 'error', content: msg }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* Panel de configuración */}
      <aside className="lg:col-span-1 space-y-4">
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
          <h3 className="font-semibold text-slate-200 mb-3 flex items-center gap-2">
            ⚙️ Configuración
          </h3>

          <label className="block text-xs text-slate-400 mb-1">Modelo</label>
          <select
            value={model}
            onChange={e => setModel(e.target.value)}
            className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm text-slate-200 mb-3"
          >
            {MODELS.map(m => <option key={m} value={m}>{m}</option>)}
          </select>

          <label className="block text-xs text-slate-400 mb-1">
            Temperatura: <span className="text-blue-400 font-mono">{temperature}</span>
          </label>
          <input
            type="range" min="0" max="2" step="0.1"
            value={temperature}
            onChange={e => setTemperature(parseFloat(e.target.value))}
            className="w-full accent-blue-500 mb-1"
          />
          <div className="flex justify-between text-xs text-slate-500 mb-3">
            <span>0 = Preciso</span><span>2 = Creativo</span>
          </div>

          <label className="block text-xs text-slate-400 mb-1">System Prompt</label>
          <select
            value={systemKey}
            onChange={e => setSystemKey(e.target.value)}
            className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm text-slate-200 mb-2"
          >
            <option value="default">🤖 Asistente LLM Expert</option>
            <option value="concise">📝 Respuestas Concisas</option>
            <option value="teacher">👨‍🏫 Profesor Universitario</option>
            <option value="formal">💼 Consultor Empresarial</option>
          </select>
          <p className="text-xs text-slate-500 italic">
            "{SYSTEM_PROMPTS[systemKey].slice(0, 60)}..."
          </p>
        </div>

        {/* Stats */}
        {stats && (
          <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
            <h3 className="font-semibold text-slate-200 mb-3">📊 Métricas</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">Tokens prompt</span>
                <span className="font-mono text-yellow-400">{stats.prompt}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Tokens respuesta</span>
                <span className="font-mono text-green-400">{stats.completion}</span>
              </div>
              <div className="flex justify-between border-t border-slate-700 pt-2">
                <span className="text-slate-400">Total tokens</span>
                <span className="font-mono text-blue-400">{stats.tokens}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Tiempo</span>
                <span className="font-mono text-purple-400">{stats.duration?.toFixed(0)}ms</span>
              </div>
            </div>
            <p className="text-xs text-slate-500 mt-3">
              💡 En APIs cloud (OpenAI/Anthropic) pagas por cada token.
              Aquí corres local = gratis ♻️
            </p>
          </div>
        )}

        {/* Preguntas sugeridas */}
        <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
          <h3 className="font-semibold text-slate-200 mb-3">💡 Preguntas de práctica</h3>
          <div className="space-y-2">
            {[
              '¿Qué es el mecanismo de atención en los transformers?',
              '¿Cuál es la diferencia entre tokens y palabras?',
              '¿Qué son los embeddings y para qué se usan?',
              '¿Qué son las alucinaciones en los LLM?',
            ].map((q, i) => (
              <button
                key={i}
                onClick={() => setInput(q)}
                className="w-full text-left text-xs text-slate-400 hover:text-blue-400 hover:bg-slate-700 rounded p-2 transition-colors"
              >
                ➤ {q}
              </button>
            ))}
          </div>
        </div>
      </aside>

      {/* Panel de chat */}
      <div className="lg:col-span-3 flex flex-col">
        <div className="bg-slate-800 rounded-xl border border-slate-700 flex flex-col h-[600px]">
          {/* Mensajes */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-slate-500">
                <span className="text-5xl mb-4">🤖</span>
                <p className="text-lg font-medium">Chat con LLM Local</p>
                <p className="text-sm">Conectado a Ollama · Sin costo · 100% privado</p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[80%] rounded-xl px-4 py-3 text-sm whitespace-pre-wrap ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : msg.role === 'error'
                    ? 'bg-red-900/50 text-red-300 border border-red-700'
                    : 'bg-slate-700 text-slate-200'
                }`}>
                  {msg.role === 'assistant' && (
                    <span className="text-xs text-slate-400 block mb-1">🤖 {model}</span>
                  )}
                  {msg.content}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-700 rounded-xl px-4 py-3">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay:'0ms'}}/>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay:'150ms'}}/>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay:'300ms'}}/>
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef}/>
          </div>

          {/* Input */}
          <div className="border-t border-slate-700 p-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                placeholder="Escribe tu pregunta sobre LLMs..."
                className="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
              <button
                onClick={sendMessage}
                disabled={loading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Enviar
              </button>
              {messages.length > 0 && (
                <button
                  onClick={() => { setMessages([]); setStats(null) }}
                  className="bg-slate-700 hover:bg-slate-600 text-slate-300 px-3 py-2 rounded-lg text-sm transition-colors"
                >
                  🗑️
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
