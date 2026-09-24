import React, { useEffect, useState } from "react";
import { api } from "../api.js";

const PROVEEDORES = ["openai", "anthropic", "google", "ollama"];

export function PanelRiesgosSesgos() {
  const [taxonomia, setTaxonomia] = useState([]);
  const [momentos, setMomentos] = useState([]);
  const [proveedor, setProveedor] = useState("ollama");
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);
  const [resultado, setResultado] = useState(null);

  useEffect(() => {
    Promise.all([api.taxonomiaRiesgo(), api.momentosMitigacion()])
      .then(([t, m]) => {
        setTaxonomia(t.taxonomia);
        setMomentos(m.momentos);
      })
      .catch((e) => setError(e.message));
  }, []);

  async function ejecutarBiasProbe() {
    setCargando(true);
    setError(null);
    try {
      const data = await api.biasProbe({ proveedor });
      setResultado(data.detalle);
    } catch (e) {
      setError(e.message);
    } finally {
      setCargando(false);
    }
  }

  return (
    <section className="panel">
      <h2>Riesgos y sesgos: principios de mitigación</h2>

      <h3>Taxonomía de riesgo (Weidinger et al., 2021)</h3>
      <table className="tabla-detalle">
        <thead>
          <tr>
            <th>Categoría</th>
            <th>Descripción</th>
            <th>Medido por</th>
          </tr>
        </thead>
        <tbody>
          {taxonomia.map((t) => (
            <tr key={t.id}>
              <td>{t.nombre}</td>
              <td>{t.descripcion}</td>
              <td>{t.medido_por}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Momentos de mitigación (Gallegos et al., 2024)</h3>
      <div className="tarjetas-resumen">
        {momentos.map((m) => (
          <div key={m.id} className="tarjeta tarjeta-texto">
            <span className="tarjeta-etiqueta">{m.nombre}</span>
            <p>{m.descripcion}</p>
          </div>
        ))}
      </div>

      <h3>Bias probe: prueba pareada</h3>
      <p className="ayuda">
        Corre 6 pares de prompts idénticos salvo por el nombre del cliente contra el
        proveedor elegido, y compara longitud y tono de las respuestas — una señal
        heurística de trato diferencial, no una auditoría de sesgo completa.
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
        <button onClick={ejecutarBiasProbe} disabled={cargando}>
          {cargando ? "Ejecutando…" : "Ejecutar bias probe"}
        </button>
      </div>

      {error && <p className="error">⚠ {error}</p>}

      {resultado && (
        <div className="resultado">
          <div
            className={`resultado-banner ${resultado.resumen.alertas > 0 ? "banner-alerta" : "banner-ok"}`}
          >
            <strong>
              {resultado.resumen.alertas} de {resultado.resumen.pares_evaluados} pares con posible
              trato diferencial
            </strong>
            <p>{resultado.resumen.advertencia}</p>
          </div>

          <table className="tabla-detalle">
            <thead>
              <tr>
                <th>Categoría</th>
                <th>Nombre A</th>
                <th>Nombre B</th>
                <th>Δ Longitud %</th>
                <th>Veredicto</th>
              </tr>
            </thead>
            <tbody>
              {resultado.detalle.map((d) => (
                <tr key={d.par_id}>
                  <td>{d.categoria}</td>
                  <td>{d.nombre_a}</td>
                  <td>{d.nombre_b}</td>
                  <td>{d.diferencia_longitud_pct}%</td>
                  <td className={d.veredicto.startsWith("POSIBLE") ? "riesgo riesgo-alto" : ""}>
                    {d.veredicto.startsWith("POSIBLE") ? "Revisar" : "Sin señal"}
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
