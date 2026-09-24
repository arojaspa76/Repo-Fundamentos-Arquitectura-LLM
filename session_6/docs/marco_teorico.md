# Marco teórico: Costos por Tokens/Latencia, Riesgos/Sesgos y Selección de Alternativa

Este documento fundamenta las decisiones de diseño del código en `backend/`, con las citas verificables detrás de cada una.

## 1. Por qué percentiles y no promedios (modelo de costos por latencia)

La Sesión 5 introdujo el costo por token. Esta sesión agrega la segunda mitad del "objetivo de desempeño" del curso: el tiempo. La práctica estándar en sistemas distribuidos de producción es reportar latencia en percentiles (P50, P95, P99), no en promedio. Dean, J. & Barroso, L. A. (2013), "The Tail at Scale", *Communications of the ACM*, 56(2), 74-80, explican por qué: en un sistema con múltiples componentes encadenados, la experiencia del usuario está dominada por el componente más lento de la cadena en el **peor caso**, no en el caso típico — un promedio de 800ms puede esconder que 1 de cada 20 llamadas tarda 6 segundos, y esa cola (`tail latency`) es la que rompe la experiencia real.

`modelo_costos.py` implementa esto directamente: `calcular_perfil_latencia()` nunca devuelve solo un promedio, siempre P50/P95/P99/mínimo/máximo. Y `calcular_costo_efectivo()` combina el costo monetario con la tasa de incumplimiento de un SLA definido por el equipo — porque el proveedor "más barato por token" puede no serlo si el 20% de sus respuestas rompen la expectativa de tiempo del usuario.

## 2. Riesgos: de "sesgo" como palabra vaga a una taxonomía operativa

Antes de medir riesgo, un equipo necesita un vocabulario común. Weidinger, L. et al. (2021), "Ethical and social risks of harm from Language Models" (arXiv:2112.04359, DeepMind; publicado también como "Taxonomy of Risks posed by Language Models" en ACM FAccT 2022), propone 6 categorías que van mucho más allá de "el modelo dice algo ofensivo": discriminación/exclusión, riesgos de información, desinformación, usos maliciosos, daños en la interacción humano-máquina, y daños ambientales/socioeconómicos.

`riesgos_sesgos.py` expone esta taxonomía completa (`TAXONOMIA_RIESGO_WEIDINGER`) y, deliberadamente, señala qué parte de este curso ya mide cada categoría — la mayoría no se mide con código nuevo en esta sesión, sino que ya estaba cubierta por herramientas de sesiones anteriores (OWASP de la Sesión 4, faithfulness de la Sesión 5). Esto es intencional: quiere dejar claro que "gestionar riesgo" no es una sesión aislada, es una práctica acumulativa.

## 3. Mitigación de sesgo: los tres momentos de intervención

Gallegos, I. O. et al. (2024), "Bias and Fairness in Large Language Models: A Survey" (arXiv:2309.00770, *Computational Linguistics*, MIT Press), organiza décadas de investigación sobre mitigación de sesgo en tres momentos: **pre-procesamiento** (antes de la llamada: prompts neutros, instrucciones explícitas de equidad), **en-procesamiento** (durante la generación: decodificación controlada, temperatura), y **post-procesamiento** (después de la respuesta: pruebas automatizadas, revisión humana, filtros).

`riesgos_sesgos.py` expone estos tres momentos (`MOMENTOS_MITIGACION`) e implementa una herramienta de post-procesamiento: el **bias probe pareado**. La técnica ("counterfactual input pairs") consiste en generar el mismo prompt cambiando solo un atributo del cliente (en este caso, el nombre, que sugiere género/origen percibido) y comparar las respuestas. Si hay una diferencia sistemática de tono o longitud sin una razón legítima relacionada con la tarea, es una señal de trato diferencial. `comparar_par()` implementa esta comparación de forma heurística (longitud + léxico de tono) — **no es un análisis estadístico riguroso**, es una primera señal barata, exactamente con el mismo espíritu del harness ligero de evaluación de la Sesión 5.

## 4. Selección de alternativa: de cuatro señales a una decisión

Las Sesiones 5 y 6 producen cuatro señales independientes sobre cada proveedor candidato: calidad (Sesión 5), costo (Sesión 5/6), latencia (Sesión 6) y riesgo de sesgo (Sesión 6). Ninguna por sí sola basta para decidir. `seleccion_alternativa.py` implementa una versión simplificada ("AHP-lite") del Proceso de Jerarquía Analítica de Saaty, T. L. (1980), *The Analytic Hierarchy Process (AHP) for Decision Making*, McGraw-Hill — el método de referencia en investigación de operaciones para decisiones con múltiples criterios.

La simplificación frente al AHP completo es deliberada y se documenta explícitamente en el código: en vez de construir la matriz de comparaciones por pares entre todos los criterios que exige el método original, el equipo asigna directamente un peso 0-1 a cada criterio (que deben sumar 1). Es más rápido de aplicar en un PoC, al costo de ser menos riguroso matemáticamente — un estudiante de nivel Maestría debe entender esa diferencia y saber cuándo el AHP completo sí vale la pena (decisiones de alto impacto con múltiples stakeholders que pueden no estar de acuerdo en los pesos).

Un detalle de diseño importante: `calcular_ranking()` normaliza cada criterio a una escala 0-1 donde "mayor es mejor" antes de ponderar — costo, latencia y tasa de sesgo se invierten (`_normalizar_menor_es_mejor`) porque en esos tres, el valor más bajo es el mejor resultado. Combinar magnitudes de distinta naturaleza (USD, segundos, proporción 0-1) sin normalizar primero es un error común que hace que el criterio con la escala numérica más grande domine el puntaje sin que eso sea la intención real de los pesos.

## 5. Conexión con las sesiones anteriores

Esta sesión no introduce un PoC nuevo: reutiliza el dominio de "Tienda Andina" (Sesiones 4 y 5) y los adaptadores de proveedor de la Sesión 5 (`proveedores.py`, sin cambios). La taxonomía de riesgo conecta explícitamente con OWASP (Sesión 4) y faithfulness/RAGAS (Sesión 5). El objetivo es que el estudiante vea el Capítulo 3 como una sola línea de razonamiento — evaluar, costear, gestionar riesgo, decidir — no como módulos aislados.
