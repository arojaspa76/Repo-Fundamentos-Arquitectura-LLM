import { useState, useRef, useEffect } from 'react'

const API_BASE = 'http://localhost:8000'

// ── Componente: Burbuja de mensaje ───────────────────────────────────────────
function Mensaje({ msg }) {
  const esUsuario = msg.role === 'user'
  return (
    <div className={`flex ${esUsuario ? 'justify-end' : 'justify-start'} mb-3`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          esUsuario
            ? 'bg-blue-600 text-white rounded-br-sm'
            : 'bg-gray-700 text-gray-100 rounded-bl-sm'
        }`}
      >
        {/* Icono del rol */}
        <div className={`text-xs font-semibold mb-1 ${esUsuario ? 'text-blue-200' : 'text-green-400'}`}>
          {esUsuario ? 'Tu' : `LLM (${msg.modelo || 'llama3.2'})`}
        </div>
        {/* Contenido */}
        <p className="whitespace-pre-wrap">{msg.content}</p>
        {/* Stats del LLM */}
        {msg.tokens && (
          <div className="mt-2 text-xs text-gray-400 border-t border-gray-600 pt-1">
            {msg.tokens.total} tokens &middot; {msg.tokens.duracion_ms}ms
          </div>
        )}
      </div>
    </div>
  )
}

// ── Componente: Indicador de carga ────────────────────────────────────────────
function Cargando() {
  return (
    <div className="flex justify-start mb-3">
      <div className="bg-gray-700 rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-1">
        <span className="text-xs text-gray-400 mr-2">Generando</span>
        {[0,1,2].map(i => (
          <span key={i} className="w-2 h-2 bg-green-400 rounded-full dot-bounce" />
        ))}
      </div>
    </div>
  )
}

// ── Componente principal: App ─────────────────────────────────────────────────
export default function App() {
  const [mensajes, setMensajes] = useState([
    {
      role: 'assistant',
      content: 'Hola! Soy tu asistente LLM local (Ollama). Hazme cualquier pregunta sobre IA, Python o arquitectura de software.',
      modelo: 'llama3.2',
    }
  ])
  const [input, setInput]         = useState('')
  const [cargando, setCargando]   = useState(false)
  const [modelo, setModelo]       = useState('llama3.2')
  const [modelos, setModelos]     = useState(['llama3.2'])
  const [temperatura, setTemp]    = useState(0.7)
  const [backendOk, setBackendOk] = useState(null)
  const finRef = useRef(null)

  // Health check y listar modelos al iniciar
  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then(r => r.json())
      .then(d => setBackendOk(d.status === 'ok'))
      .catch(() => setBackendOk(false))

    fetch(`${API_BASE}/modelos`)
      .then(r => r.json())
      .then(d => {
        if (Array.isArray(d) && d.length > 0) {
          setModelos(d.map(m => m.nombre))
          setModelo(d[0].nombre)
        }
      })
      .catch(() => {})
  }, [])

  // Auto-scroll al ultimo mensaje
  useEffect(() => {
    finRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensajes, cargando])

  const enviar = async () => {
    const texto = input.trim()
    if (!texto || cargando) return

    // Agregar mensaje del usuario
    const historial = [
      { role: 'system', content: 'Eres un experto en IA, LLMs y arquitectura de software. Responde en espanol, de forma clara y concisa.' },
      ...mensajes.filter(m => m.role !== 'system').map(m => ({ role: m.role, content: m.content })),
      { role: 'user', content: texto },
    ]

    setMensajes(prev => [...prev, { role: 'user', content: texto }])
    setInput('')
    setCargando(true)

    try {
      const r = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: historial,
          model: modelo,
          temperature: temperatura,
          max_tokens: 1000,
          stream: false,
        }),
      })

      if (!r.ok) {
        const err = await r.json().catch(() => ({ detail: r.statusText }))
        throw new Error(err.detail || `HTTP ${r.status}`)
      }

      const data = await r.json()
      setMensajes(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.respuesta,
          modelo: data.modelo,
          tokens: {
            total: data.tokens_total,
            duracion_ms: data.duracion_ms,
          },
        },
      ])
    } catch (err) {
      setMensajes(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `Error: ${err.message}\n\nVerifica que el backend (uvicorn) y Ollama esten corriendo.`,
          modelo: 'error',
        },
      ])
    } finally {
      setCargando(false)
    }
  }

  const limpiar = () => {
    setMensajes([{
      role: 'assistant',
      content: 'Conversacion reiniciada. Como puedo ayudarte?',
      modelo,
    }])
  }

  return (
    <div className="flex flex-col h-screen max-w-3xl mx-auto px-4">
      {/* Header */}
      <div className="py-4 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">BSG LLM Chat</h1>
            <p className="text-xs text-gray-400">React + FastAPI + Ollama</p>
          </div>
          {/* Status indicator */}
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${backendOk === true ? 'bg-green-400' : backendOk === false ? 'bg-red-400' : 'bg-yellow-400'}`} />
            <span className="text-xs text-gray-400">
              {backendOk === true ? 'Backend OK' : backendOk === false ? 'Backend no disponible' : 'Conectando...'}
            </span>
          </div>
        </div>

        {/* Controles */}
        <div className="flex items-center gap-3 mt-3">
          <div className="flex-1">
            <label className="text-xs text-gray-400 block mb-1">Modelo</label>
            <select
              value={modelo}
              onChange={e => setModelo(e.target.value)}
              className="bg-gray-800 text-gray-100 rounded-lg px-3 py-1.5 text-sm w-full border border-gray-600"
            >
              {modelos.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
          <div className="w-32">
            <label className="text-xs text-gray-400 block mb-1">Temperatura: {temperatura}</label>
            <input
              type="range" min="0" max="1" step="0.1"
              value={temperatura}
              onChange={e => setTemp(parseFloat(e.target.value))}
              className="w-full accent-blue-500"
            />
          </div>
          <button
            onClick={limpiar}
            className="text-xs text-gray-400 hover:text-gray-200 border border-gray-600 rounded-lg px-3 py-1.5 mt-4"
          >
            Limpiar
          </button>
        </div>
      </div>

      {/* Area de mensajes */}
      <div className="flex-1 overflow-y-auto py-4">
        {mensajes.map((msg, i) => <Mensaje key={i} msg={msg} />)}
        {cargando && <Cargando />}
        <div ref={finRef} />
      </div>

      {/* Input */}
      <div className="py-4 border-t border-gray-700">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                enviar()
              }
            }}
            placeholder="Escribe tu pregunta... (Enter para enviar, Shift+Enter para nueva linea)"
            rows={2}
            className="flex-1 bg-gray-800 text-gray-100 rounded-xl px-4 py-3 text-sm resize-none border border-gray-600 focus:border-blue-500 focus:outline-none placeholder-gray-500"
          />
          <button
            onClick={enviar}
            disabled={cargando || !input.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl px-5 py-2 text-sm font-medium transition-colors"
          >
            Enviar
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2 text-center">
          Los mensajes se procesan localmente con Ollama. Ningun dato sale de tu maquina.
        </p>
      </div>
    </div>
  )
}
