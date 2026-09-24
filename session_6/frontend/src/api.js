const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8001";

async function pedir(ruta, opciones = {}) {
  const resp = await fetch(`${API_BASE}${ruta}`, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  if (!resp.ok) {
    const cuerpo = await resp.json().catch(() => ({}));
    throw new Error(cuerpo.detail || `Error HTTP ${resp.status}`);
  }
  return resp.json();
}

export const api = {
  perfilCosto: (payload) => pedir("/api/costos/perfil", { method: "POST", body: JSON.stringify(payload) }),
  taxonomiaRiesgo: () => pedir("/api/riesgos/taxonomia"),
  momentosMitigacion: () => pedir("/api/riesgos/mitigacion"),
  datasetSesgo: () => pedir("/api/riesgos/dataset-sesgo"),
  biasProbe: (payload) => pedir("/api/riesgos/bias-probe", { method: "POST", body: JSON.stringify(payload) }),
  ranking: (payload) => pedir("/api/seleccion/ranking", { method: "POST", body: JSON.stringify(payload) }),
  registro: (tipo) => pedir(`/api/registro${tipo ? `?tipo=${tipo}` : ""}`),
};
