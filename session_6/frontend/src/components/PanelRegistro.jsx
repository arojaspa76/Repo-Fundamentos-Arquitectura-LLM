import React, { useEffect, useState } from "react";
import { api } from "../api.js";

export function PanelRegistro() {
  const [corridas, setCorridas] = useState([]);
  const [filtro, setFiltro] = useState("");
  const [error, setError] = useState(null);

  async function recargar() {
    setError(null);
    try {
      const data = await api.registro(filtro || undefined);
      setCorridas(data.corridas);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    recargar();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filtro]);

  return (
    <section className="panel">
      <h2>Registro de corridas</h2>
      <p className="ayuda">
        Toda corrida de costeo/latencia, bias probe o selección de alternativa queda
        registrada aquí (backend/runs_log.json) — mismo principio de trazabilidad de la
        Sesión 5.
      </p>

      <div className="fila-controles">
        <label>
          Filtrar por tipo
          <select value={filtro} onChange={(e) => setFiltro(e.target.value)}>
            <option value="">Todos</option>
            <option value="costeo_latencia">costeo_latencia</option>
            <option value="bias_probe">bias_probe</option>
            <option value="seleccion">seleccion</option>
          </select>
        </label>
        <button onClick={recargar}>Actualizar</button>
      </div>

      {error && <p className="error">⚠ {error}</p>}

      <table className="tabla-detalle">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Tipo</th>
            <th>Aprobado por</th>
          </tr>
        </thead>
        <tbody>
          {corridas
            .slice()
            .reverse()
            .map((run) => (
              <tr key={run.id}>
                <td>{new Date(run.timestamp).toLocaleString()}</td>
                <td>{run.tipo}</td>
                <td>{run.aprobado_por || "—"}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </section>
  );
}
