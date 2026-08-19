/**
 * App.jsx — Componente raíz de la aplicación
 * ============================================
 * Organiza las tres herramientas educativas de la Sesión 1:
 * 1. Chat Interface    — Interactuar con el LLM local
 * 2. Token Visualizer  — Ver cómo se tokeniza el texto
 * 3. Embedding Explorer — Explorar similitud semántica
 */

import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import TokenVisualizer from './components/TokenVisualizer'
import EmbeddingExplorer from './components/EmbeddingExplorer'

const TABS = [
  { id: 'chat',       label: '💬 Chat con LLM',        desc: 'Interactúa con el modelo local' },
  { id: 'tokens',     label: '🔤 Tokenizador',          desc: 'Visualiza cómo se dividen los tokens' },
  { id: 'embeddings', label: '🧭 Embeddings',            desc: 'Explora similitud semántica' },
]

export default function App() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-800/50 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🤖</span>
            <div>
              <h1 className="text-xl font-bold text-white">
                Fundamentos de Arquitectura LLM
              </h1>
              <p className="text-sm text-slate-400">
                Sesión 1 — Arquitectura y Componentes Esenciales · Ollama Local
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs de navegación */}
      <nav className="border-b border-slate-700 bg-slate-800/30">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex gap-1">
            {TABS.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-5 py-3 text-sm font-medium transition-colors border-b-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-400 bg-blue-500/10'
                    : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-700/30'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Contenido principal */}
      <main className="max-w-6xl mx-auto px-4 py-6">
        {activeTab === 'chat'       && <ChatInterface />}
        {activeTab === 'tokens'     && <TokenVisualizer />}
        {activeTab === 'embeddings' && <EmbeddingExplorer />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700 mt-12 py-4">
        <div className="max-w-6xl mx-auto px-4 text-center text-xs text-slate-500">
          Curso Fundamentos de Arquitectura LLM · BSG Institute ·
          Backend: FastAPI en localhost:8000 · LLM: Ollama local
        </div>
      </footer>
    </div>
  )
}
