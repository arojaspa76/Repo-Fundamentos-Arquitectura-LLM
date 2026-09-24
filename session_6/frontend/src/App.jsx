import React, { useState } from "react";
import { PanelCostoLatencia } from "./components/PanelCostoLatencia.jsx";
import { PanelRiesgosSesgos } from "./components/PanelRiesgosSesgos.jsx";
import { PanelSeleccion } from "./components/PanelSeleccion.jsx";
import { PanelRegistro } from "./components/PanelRegistro.jsx";

const PESTANAS = [
  { id: "costos", etiqueta: "1. Costo por Tokens/Latencia" },
  { id: "riesgos", etiqueta: "2. Riesgos y Sesgos" },
  { id: "seleccion", etiqueta: "3. Selección de Alternativa" },
  { id: "registro", etiqueta: "4. Registro de Corridas" },
];

export default function App() {
  const [pestanaActiva, setPestanaActiva] = useState("costos");

  return (
    <div className="app">
      <header className="app-header">
        <p className="eyebrow">Fundamentos de Arquitectura LLM · Capítulo 3 · Sesión 6</p>
        <h1>Costos por Tokens/Latencia, Riesgos/Sesgos y Selección de Alternativa</h1>
        <p className="subtitulo">
          Cierra la decisión que las Sesiones 5 y 6 vienen preparando: qué proveedor base
          usar para el PoC de "Tienda Andina", con evidencia de costo, latencia y sesgo.
        </p>
      </header>

      <nav className="tabs">
        {PESTANAS.map((p) => (
          <button
            key={p.id}
            className={p.id === pestanaActiva ? "tab tab-activo" : "tab"}
            onClick={() => setPestanaActiva(p.id)}
          >
            {p.etiqueta}
          </button>
        ))}
      </nav>

      <main className="contenido">
        {pestanaActiva === "costos" && <PanelCostoLatencia />}
        {pestanaActiva === "riesgos" && <PanelRiesgosSesgos />}
        {pestanaActiva === "seleccion" && <PanelSeleccion />}
        {pestanaActiva === "registro" && <PanelRegistro />}
      </main>
    </div>
  );
}
