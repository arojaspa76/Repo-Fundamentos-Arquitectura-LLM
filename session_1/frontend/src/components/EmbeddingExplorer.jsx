/**
 * EmbeddingExplorer.jsx
 * ======================
 * Demuestra visualmente la similitud semántica entre textos
 * usando embeddings vectoriales de Ollama (nomic-embed-text).
 * Los estudiantes verán que palabras relacionadas tienen
 * alta similitud aunque no compartan letras.
 */

import { useState } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

const PRESET_PAIRS = [
  { label: 'Sinónimos',      t1: 'automóvil', t2: 'carro', expect: 'alta' },
  { label: 'Categoría',      t1: 'perro', t2: 'gato', expect: 'alta' },
  { label: 'Relacionados',   t1: 'inteligencia artificial', t2: 'machine learning', expect: 'alta' },
  { label: 'Sin relación',   t1: 'pizza', t2: 'física cuántica', expect: 'baja' },
  { label: 'Opuestos',       t1: 'amor', t2: 'odio', expect: 'media' },
  { label: 'ES vs EN',       t1: 'inteligencia artificial', t2: 'artificial intelligence', expect: 'muy alta' },
]

function SimilarityBar({ score }) {
  const pct = Math.max(0, Math.min(1, score)) * 100
  const color = score >= 0.85 ? 'bg-green-500' :
                score >= 0.70 ? 'bg-yellow-500' :
                score >= 0.50 ? 'bg-orange-500' : 'bg-red-500'
  return (
    <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
      <div
        className={`h-full rounded-full transition-all duration-700 ${color}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}

export default function EmbeddingExplorer() {
  const [text1, setText1]           = useState('')
  const [text2, setText2]           = useState('')
  const [result, setResult]         = useState(null)
  const [loading, setLoading]       = useState(false)
  const [error, setError]           = useState('')
  const [batchResults, setBatchResults] = useState(null)
  const [batchLoading, setBatchLoading] = useState(false)

  const compare = async (t1 = text1, t2 = text2) => {
    if (!t1.trim() || !t2.trim()) return
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const res = await axios.post(`${API_URL}/similarity`, {
        text1: t1, text2: t2, model: 'nomic-embed-text'
      })
      setResult(res.data)
    } catch (err) {
      const detail = err.response?.data?.detail
      if (typeof detail === 'string' && detail.includes('nomic')) {
        setError('Modelo no encontrado. Ejecuta: ollama pull nomic-embed-text')
      } else {
        setError(detail || 'Error al conectar con el servidor')
      }
    } finally {
      setLoading(false)
    }
  }

  const runBatch = async () => {
    setBatchLoading(true)
    setBatchResults(null)
    try {
      const results = await Promise.all(
        PRESET_PAIRS.map(p =>
          axios.post(`${API_URL}/similarity`, {
            text1: p.t1, text2: p.t2, model: 'nomic-embed-text'
          }).then(r => ({ ...p, ...r.data }))
        )
      )
      setBatchResults(results)
    } catch (err) {
      setError('Error en comparación masiva. ¿Está instalado nomic-embed-text?')
    } finally {
      setBatchLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Intro educativa */}
      <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
        <h2 className="text-lg font-bold text-white mb-2">🧭 Explorador de Embeddings</h2>
        <p className="text-sm text-slate-400">
          Los <strong className="text-purple-400">embeddings</strong> convierten texto en vectores numéricos
          en un espacio de alta dimensión (768D en nomic-embed-text).
          Textos con significados similares estarán <strong className="text-purple-400">cercanos</strong> en ese espacio.
          Medimos esa cercanía con la <strong className="text-purple-400">similitud coseno</strong> [0 a 1].
        </p>
        <p className="text-xs text-slate-500 mt-2">
          🔧 Requiere: <code className="bg-slate-700 px-1 rounded">ollama pull nomic-embed-text</code>
        </p>
      </div>

      {/* Comparador manual */}
      <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
        <h3 className="font-semibold text-slate-200 mb-4">Comparar dos textos</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-xs text-slate-400 mb-1">Texto 1</label>
            <input
              value={text1}
              onChange={e => setText1(e.target.value)}
              placeholder="ej: inteligencia artificial"
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-400 mb-1">Texto 2</label>
            <input
              value={text2}
              onChange={e => setText2(e.target.value)}
              placeholder="ej: machine learning"
              className="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {PRESET_PAIRS.map((p, i) => (
            <button
              key={i}
              onClick={() => { setText1(p.t1); setText2(p.t2); compare(p.t1, p.t2) }}
              className="text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 px-3 py-1.5 rounded-full transition-colors"
            >
              {p.label}
            </button>
          ))}
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => compare()}
            disabled={loading || !text1.trim() || !text2.trim()}
            className="bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {loading ? 'Calculando...' : '🔍 Calcular Similitud'}
          </button>
          <button
            onClick={runBatch}
            disabled={batchLoading}
            className="bg-slate-700 hover:bg-slate-600 text-slate-300 px-5 py-2 rounded-lg text-sm transition-colors"
          >
            {batchLoading ? 'Ejecutando...' : '📊 Comparación masiva'}
          </button>
        </div>

        {error && (
          <div className="mt-3 bg-red-900/30 border border-red-700/50 rounded-lg p-3">
            <p className="text-red-300 text-sm">❌ {error}</p>
            <code className="text-xs text-slate-400 mt-1 block">ollama pull nomic-embed-text</code>
          </div>
        )}
      </div>

      {/* Resultado individual */}
      {result && (
        <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-200">Resultado</h3>
            <span className={`text-3xl font-bold font-mono ${
              result.similarity >= 0.85 ? 'text-green-400' :
              result.similarity >= 0.70 ? 'text-yellow-400' :
              result.similarity >= 0.50 ? 'text-orange-400' : 'text-red-400'
            }`}>
              {(result.similarity * 100).toFixed(1)}%
            </span>
          </div>

          <div className="flex items-center gap-3 mb-4">
            <span className="text-sm bg-slate-700 px-3 py-1 rounded-full font-mono">"{result.text1}"</span>
            <span className="text-slate-500">↔</span>
            <span className="text-sm bg-slate-700 px-3 py-1 rounded-full font-mono">"{result.text2}"</span>
          </div>

          <SimilarityBar score={result.similarity} />

          <p className="text-sm text-slate-300 mt-3">{result.interpretation}</p>

          <div className="mt-4 bg-slate-700/50 rounded-lg p-3 text-xs text-slate-400">
            <strong>¿Qué significa esto?</strong> El modelo nomic-embed-text convirtió cada texto en
            un vector de 768 números. Luego calculamos el coseno del ángulo entre esos vectores.
            Un ángulo pequeño = alta similitud semántica.
          </div>
        </div>
      )}

      {/* Comparación masiva */}
      {batchResults && (
        <div className="bg-slate-800 rounded-xl p-5 border border-slate-700">
          <h3 className="font-semibold text-slate-200 mb-4">📊 Resultados: Comparación Masiva</h3>
          <div className="space-y-3">
            {batchResults.map((r, i) => (
              <div key={i} className="bg-slate-700/50 rounded-lg p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm">
                    <span className="text-slate-400">{r.label}: </span>
                    <span className="font-mono text-purple-300">"{r.text1}"</span>
                    <span className="text-slate-500 mx-2">↔</span>
                    <span className="font-mono text-purple-300">"{r.text2}"</span>
                  </div>
                  <span className={`font-mono font-bold text-sm ml-3 whitespace-nowrap ${
                    r.similarity >= 0.85 ? 'text-green-400' :
                    r.similarity >= 0.70 ? 'text-yellow-400' :
                    r.similarity >= 0.50 ? 'text-orange-400' : 'text-red-400'
                  }`}>
                    {(r.similarity * 100).toFixed(1)}%
                  </span>
                </div>
                <SimilarityBar score={r.similarity} />
              </div>
            ))}
          </div>
          <p className="text-xs text-slate-500 mt-4">
            💡 Observa: "inteligencia artificial" y "artificial intelligence" tienen similitud muy alta
            aunque estén en idiomas diferentes. Los embeddings capturan SIGNIFICADO, no letras.
          </p>
        </div>
      )}
    </div>
  )
}
