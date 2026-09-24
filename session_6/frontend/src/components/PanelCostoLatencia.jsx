import React, { useState } from "react";
import { api } from "../api.js";

const PROVEEDORES = ["openai", "anthropic", "google", "ollama"];

export function PanelCostoLatencia() {
  const [proveedor, setProveedor] = useState("ollama");
  const [numLlamadas, setNumLlamadas] = useState(10);
  const [umbralSla, setUmbralSla] = useState(3.0);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  const [resultado, setResultado] = useState(null);

  async function ejecutar() {
    setCargando(true);
    setError(null);
    try {
      const data = await api.perfilCosto({
        proveedor,
        num_llamadas: Number(numLlamadas),
        umbral_sla_segundos: Number(umbralSla),
        aprobado_por: undefined,
      });
      setResultado(data.detalle);
    } catch (e) {
      setError(e.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <section className="panel">
      <h2>Perfil de costo y latencia</h2>
      <p className="ayuda">
        Corre N llamadas contra el proveedor elegido y calcula el costo promedio junto con
        percentiles de latencia (P50/P95/P99) — nunca solo el promedio (Dean &amp; Barroso,
        2013, "The Tail at Scale"). También calcula qué fracción de llamadas incumple el
        umbral de SLA que definas.
      </p>

      <div className="fila-controles">
        <label>
          Proveedor
          <select value={proveedor} onChange={(e) => setProveedor(e.target.value)}>
            {PROVEEDORES.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </label>
        <label>
          Nº de llamadas
          <input
            type="number"
            min="3"
            max="50"
            value={numLlamadas}
            onChange={(e) => setNumLlamadas(e.target.value)}
          />
        </label>
        <label>
          Umbral SLA (segundos)
          <input
            type="number"
            step="0.1"
            value={umbralSla}
            onChange={(e) => setUmbralSla(e.target.value)}
          />
        </label>
        <button onClick={ejecutar} disabled={cargando}>
          {cargando ? "Ejecutando…" : "Ejecutar perfil"}
        </button>
      </div>

      {error && <p className="error">⚠ {error}</p>}

      {resultado && (
        <div className="resultado">
          <div className="tarjetas-resumen">
            <div className="tarjeta">
              <span className="tarjeta-valor">${resultado.costo_promedio_usd}</span>
              <span className="tarjeta-etiqueta">Costo promedio / llamada (USD)</span>
            </div>
            <div className="tarjeta">
              <span className="tarjeta-valor">{resultado.perfil_latencia.p50_segundos}s</span>
              <span className="tarjeta-etiqueta">P50 (mediana)</span>
            </div>
            <div className="tarjeta">
              <span className="tarjeta-valor">{resultado.perfil_latencia.p95_segundos}s</span>
              <span className="tarjeta-etiqueta">P95</span>
            </div>
            <div className="tarjeta">
              <span className="tarjeta-valor">{resultado.perfil_latencia.p99_segundos}s</span>
              <span className="tarjeta-etiqueta">P99 (cola)</span>
            </div>
          </div>

          <div className={`resultado-banner ${resultado.costo_efectivo.tasa_incumplimiento_sla > 0.05 ? "banner-alerta" : "banner-ok"}`}>
            <strong>
              {(resultado.costo_efectivo.tasa_incumplimiento_sla * 100).toFixed(1)}% de llamadas incumplen el SLA de{" "}
              {resultado.costo_efectivo.umbral_sla_segundos}s
            </strong>
            <p>{resultado.costo_efectivo.interpretacion}</p>
          </div>
        </div>
      )}
    </section>
  );
}
