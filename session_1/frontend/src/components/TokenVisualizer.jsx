/**
 * TokenVisualizer.jsx
 * ====================
 * Herramienta educativa que muestra visualmente cómo un LLM
 * divide el texto en tokens. Compara español vs inglés y muestra
 * el impacto del costo en APIs cloud.
 */

import { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

const COLORS = [
  'bg-blue-500/20 border-blue-500/50 text-blue-300',
  'bg-purple-500/20 border-purple-500/50 text-purple-300',
  'bg-green-500/20 border-green-500/50 text-green-300',
  'bg-orange-500/20 border-orange-500/50 text-orange-300',
  'bg-pink-500/20 border-pink-500/50 text-pink-300',
  'bg-teal-500/20 border-teal-500/50 text-teal-300',
  'bg-yellow-500/20 border-yellow-500/50 text-yellow-300',
  'bg-red-500/20 border-red-500/50 text-red-300',
]

const EXAMPLES = [
  { label: '🇪🇸 Español técnico', text: 'Los modelos de lenguaje grande son sistemas de inteligencia artificial basados en redes neuronales transformadoras.' },
  { label: '🇺🇸 English technical', text: 'Large language models are artificial intelligence systems based on transformer neural networks.' },
  { label: '💻 Código Python',     text: 'def generate_embedding(text: str) -> list[float]:\n    return model.encode(text).tolist()' },
  { label: '🔢 Números y datos',   text: 'El modelo procesó 1,234,567 tokens en 2.5 segundos a un costo de $0.002 por 1K tokens.' },
  { label: '😊 Emojis y special',  text: '¡Hola! 🤖 Este es un ejemplo con caracteres especiales: ñ, á, é, ü, ß, 中文, عربي' },
]

export default function TokenVisualizer() {
  const [text, setText]       = useState('')
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')
  const [compare, setCompare] = useState(null)

  const tokenize = async (inputText = text) => {
    if (!inputText.trim()) return
    setLoading(true)
    setError('')
    try {
      const res = await axios.post(`${API_URL}/tokenize`, { text: inputText })
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al conectar con el servidor')
    } finally {
      setLoading(false)
    }
  }

  const runComparison = async () => {
    const es = 'Los modelos de lenguaje procesan texto como secuencias de tokens'
    const en = 'Language models process text as sequences of tokens'
    const [resEs, resEn] = await Promise.all([
      axios.post(`${API_URL}/tokenize`, { text: es }),
      axios.post(`${API_URL}/tokenize`, { text: en }),
    ])
    setCompare({ es: { text: es, ...resEs.data }, en: { text: en, ...resEn.data } })
  }

  return (
    <div className="space-y-6">
      {/* Título educativo */}
      <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
        <h2 className="text-lg font-bold text-white mb-2">🔤 Visualizador de Tokens</h2>
        <p className="text-sm text-slate-400">
          Los LLMs no procesan palabras completas — dividen el texto en <strong className="text-blue-400">tokens</strong>,
          que pueden ser partes de palabras, signos de puntuación o espacios.
          Un token equivale aproximadamente a <strong className="text-blue-400">0.75 palabras en inglés</strong> o
          <strong className="text-blue-400"> 0.6 palabras en español</strong>.
        </p>
      </div>

      {/* Input */}
      <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
        <div className="flex flex-wrap gap-2 mb-3">
          {EXAMPLES.map((ex, i) => (
            <button
              key={i}
              onClick={() => { setText(ex.text); tokenize(ex.text) }}
              className="text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 px-3 py-1.5 rounded-full transition-colors"
            >
              {ex.label}
            </button>
          ))}
        </div>

        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Escribe o pega cualquier texto para ver cómo se tokeniza..."
          rows={3}
          className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 resize-none mb-3"
        />

        <div className="flex gap-3">
          <button
            onClick={() => tokenize()}
            disabled={loading || !text.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {loading ? 'Tokenizando...' : '🔍 Tokenizar'}
          </button>
          <button
            onClick={runComparison}
            className="bg-slate-700 hover:bg-slate-600 text-slate-300 px-5 py-2 rounded-lg text-sm transition-colors"
          >
            📊 Comparar ES vs EN
          </button>
        </div>

        {error && <p className="text-red-400 text-sm mt-3">❌ {error}</p>}
      </div>

      {/* Resultado */}
      {result && (
        <div className="space-y-4">
          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { label: 'Tokens', value: result.token_count, color: 'text-blue-400' },
              { label: 'Palabras', value: result.word_count, color: 'text-green-400' },
              { label: 'Caracteres', value: result.char_count, color: 'text-yellow-400' },
              { label: 'Tokens/Palabra', value: result.tokens_per_word, color: 'text-purple-400' },
            ].map((stat, i) => (
              <div key={i} className="bg-slate-800 rounded-xl p-4 border border-slate-700 text-center">
                <div className={`text-2xl font-bold font-mono ${stat.color}`}>
                  {stat.value}
                </div>
                <div className="text-xs text-slate-400 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>

          {/* Tokens visualizados */}
          <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
            <h3 className="font-semibold text-slate-200 mb-3">
              Vista de tokens (primeros 20)
            </h3>
            <div className="flex flex-wrap gap-1">
              {result.tokens_preview.map((token, i) => (
                <span
                  key={i}
                  className={`token-chip border ${COLORS[i % COLORS.length]} px-2 py-1 rounded text-xs font-mono`}
                >
                  {token}
                </span>
              ))}
              {result.token_count > 20 && (
                <span className="text-slate-500 text-xs px-2 py-1">
                  + {result.token_count - 20} tokens más...
                </span>
              )}
            </div>
          </div>

          {/* Nota educativa */}
          <div className="bg-blue-900/20 border border-blue-700/50 rounded-xl p-4">
            <p className="text-sm text-blue-300">{result.educational_note}</p>
          </div>

          {/* Costo estimado */}
          <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
            <h3 className="font-semibold text-slate-200 mb-3">💰 Costo estimado en APIs cloud</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
              {[
                { provider: 'OpenAI GPT-4o-mini', price: 0.15, color: 'text-green-400' },
                { provider: 'OpenAI GPT-4o',      price: 2.50, color: 'text-yellow-400' },
                { provider: 'Anthropic Claude 3.5 Sonnet', price: 3.00, color: 'text-orange-400' },
              ].map((p, i) => (
                <div key={i} className="bg-slate-700/50 rounded-lg p-3">
                  <div className="font-medium text-slate-300">{p.provider}</div>
                  <div className={`font-mono font-bold ${p.color}`}>
                    ${((result.token_count / 1000) * p.price).toFixed(6)} USD
                  </div>
                  <div className="text-xs text-slate-500">${p.price}/1M tokens input</div>
                </div>
              ))}
            </div>
            <p className="text-xs text-slate-500 mt-3">
              ♻️ Con Ollama local: $0.00 USD · Sin límites · Sin latencia de red
            </p>
          </div>
        </div>
      )}

      {/* Comparación ES vs EN */}
      {compare && (
        <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
          <h3 className="font-semibold text-slate-200 mb-4">
            📊 ¿Por qué el español usa más tokens?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { lang: '🇪🇸 Español', data: compare.es, color: 'bg-red-500' },
              { lang: '🇺🇸 English', data: compare.en, color: 'bg-blue-500' },
            ].map(({ lang, data, color }, i) => (
              <div key={i} className="bg-slate-700/50 rounded-lg p-4">
                <div className="font-medium text-slate-200 mb-2">{lang}</div>
                <p className="text-xs text-slate-400 italic mb-3">"{data.text}"</p>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Tokens</span>
                  <span className="font-mono text-white font-bold">{data.token_count}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Palabras</span>
                  <span className="font-mono text-slate-300">{data.word_count}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Tokens/Palabra</span>
                  <span className={`font-mono font-bold ${data.tokens_per_word > 1.3 ? 'text-orange-400' : 'text-green-400'}`}>
                    {data.tokens_per_word}
                  </span>
                </div>
              </div>
            ))}
          </div>
          <p className="text-xs text-slate-500 mt-4">
            💡 Los LLMs fueron entrenados principalmente con texto en inglés.
            El vocabulario tokenizador es más eficiente en inglés.
            Por eso los textos en español/chino/árabe son proporcionalmente más caros.
          </p>
        </div>
      )}
    </div>
  )
}
