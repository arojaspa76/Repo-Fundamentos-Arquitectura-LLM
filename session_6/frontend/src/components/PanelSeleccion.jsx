import React, { useState } from "react";
import { api } from "../api.js";

const CANDIDATOS_INICIALES = [
  { proveedor: "openai", modelo: "gpt-4o-mini", puntaje_calidad: 0.85, costo_promedio_usd: 0.0009, latencia_p95_segundos: 1.4, tasa_alerta_sesgo: 0.0 },
  { proveedor: "anthropic", modelo: "claude-haiku-4-5", puntaje_calidad: 0.88, costo_promedio_usd: 0.0025, latencia_p95_segundos: 1.1, tasa_alerta_sesgo: 0.0 },
  { proveedor: "ollama", modelo: "llama3.2", puntaje_calidad: 0.55, costo_promedio_usd: 0.0, latencia_p95_segundos: 3.8, tasa_alerta_sesgo: 0.17 },
];

const PESOS_INICIALES = { calidad: 0.35, costo: 0.30, latencia: 0.20, riesgo_sesgo: 0.15 };

export function PanelSeleccion() {
  const [candidatos, setCandidatos] = useState(CANDIDATOS_INICIALES);
  const [pesos, setPesos] = useState(PESOS_INICIALES);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);

  function actualizarCandidato(index, campo, valor) {
    setCandidatos((prev) =>
      prev.map((c, i) => (i === index ? { ...c, [campo]: campo === "proveedor" || campo === "modelo" ? valor : Number(valor) } : c))
    );
  }

  function actualizarPeso(criterio, valor) {
    setPesos((prev) => ({ ...prev, [criterio]: Number(valor) }));
  }

  const sumaPesos = Object.values(pesos).reduce((a, b) => a + b, 0);

  async function calcular() {
    setError(null);
    try {
      const data = await api.ranking({ candidatos, pesos });
      setResultado(data.detalle);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <section className="panel">
      <h2>Selección de alternativa base (matriz de decisión ponderada)</h2>
      <p className="ayuda">
        Combina calidad, costo, latencia (P95) y tasa de alerta de sesgo en un puntaje
        ponderado único — versión simplificada del AHP de Saaty (1980). Ajusta los pesos
        y los candidatos con datos reales de las pestañas anteriores.
      </p>

      <h3>Candidatos</h3>
      <table className="tabla-detalle tabla-editable">
        <thead>
          <tr>
            <th>Proveedor</th>
            <th>Modelo</th>
            <th>Calidad (0-1)</th>
            <th>Costo prom. (USD)</th>
            <th>Latencia P95 (s)</th>
            <th>Tasa alerta sesgo (0-1)</th>
          </tr>
        </thead>
        <tbody>
          {candidatos.map((c, i) => (
            <tr key={i}>
              <td>
                <input value={c.proveedor} onChange={(e) => actualizarCandidato(i, "proveedor", e.target.value)} />
              </td>
              <td>
                <input value={c.modelo} onChange={(e) => actualizarCandidato(i, "modelo", e.target.value)} />
              </td>
              <td>
                <input type="number" step="0.01" min="0" max="1" value={c.puntaje_calidad} onChange={(e) => actualizarCandidato(i, "puntaje_calidad", e.target.value)} />
              </td>
              <td>
                <input type="number" step="0.0001" min="0" value={c.costo_promedio_usd} onChange={(e) => actualizarCandidato(i, "costo_promedio_usd", e.target.value)} />
              </td>
              <td>
                <input type="number" step="0.1" min="0" value={c.latencia_p95_segundos} onChange={(e) => actualizarCandidato(i, "latencia_p95_segundos", e.target.value)} />
              </td>
              <td>
                <input type="number" step="0.01" min="0" max="1" value={c.tasa_alerta_sesgo} onChange={(e) => actualizarCandidato(i, "tasa_alerta_sesgo", e.target.value)} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Pesos (deben sumar 1.0 — suma actual: {sumaPesos.toFixed(2)})</h3>
      <div className="fila-controles">
        {Object.entries(pesos).map(([criterio, valor]) => (
          <label key={criterio}>
            {criterio}
            <input type="number" step="0.05" min="0" max="1" value={valor} onChange={(e) => actualizarPeso(criterio, e.target.value)} />
          </label>
        ))}
        <button onClick={calcular} disabled={Math.abs(sumaPesos - 1) > 0.01}>
          Calcular ranking
        </button>
      </div>

      {error && <p className="error">⚠ {error}</p>}

      {resultado && (
        <div className="resultado">
          <div className="resultado-banner banner-ok">
            <strong>Recomendación: {resultado.recomendacion.alternativa_recomendada}</strong>
            <p>{resultado.recomendacion.nota_confianza}</p>
          </div>

          <table className="tabla-detalle">
            <thead>
              <tr>
                <th>#</th>
                <th>Proveedor</th>
                <th>Modelo</th>
                <th>Calidad norm.</th>
                <th>Costo norm.</th>
                <th>Latencia norm.</th>
                <th>Riesgo norm.</th>
                <th>Puntaje total</th>
              </tr>
            </thead>
            <tbody>
              {resultado.ranking.map((r, i) => (
                <tr key={`${r.proveedor}:${r.modelo}`} className={i === 0 ? "fila-ganadora" : ""}>
                  <td>{i + 1}</td>
                  <td>{r.proveedor}</td>
                  <td>{r.modelo}</td>
                  <td>{r.puntaje_calidad_normalizado}</td>
                  <td>{r.puntaje_costo_normalizado}</td>
                  <td>{r.puntaje_latencia_normalizado}</td>
                  <td>{r.puntaje_riesgo_normalizado}</td>
                  <td>
                    <strong>{r.puntaje_ponderado_total}</strong>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
