# 🌿 LivLin · Indagación Regenerativa v7.1

**Potencial para una vida regenerativa** · www.livlin.cl

## Cambios v7.1 (sobre v7.0)

### Sidebar del cliente mejorado
El sidebar de la vista de usuarios tiene 3 secciones bien definidas:
- **A) Logo + Secciones del informe** — botones de navegación
- **B) Descargar informe** — Excel y Word
- **C) Cerrar sesión**

### Perspectiva Comparada completa
La pestaña "Perspectiva Comparada" ahora contiene **toda la información** de las pestañas ERP y HRP:
- Radar dual (ERP + HRP superpuestos)
- Barras apiladas de 7 pétalos y 10 dimensiones
- Radar independiente ERP con interpretaciones por pétalo
- Sub-indicadores M2-6 con transparencia
- Radar independiente HRP con interpretaciones por pétalo
- Metodología de cálculo

### Fotos restauradas en vista cliente
La sección de Registro Fotográfico ahora carga las fotos desde Supabase/tmp (restaurado de v6).

### Explicaciones profundas de pétalos
Cada pétalo de la Flor de la Permacultura incluye:
- Nombre original de Holmgren (2002)
- Resumen descriptivo
- Detalle extenso
- Referencias bibliográficas específicas del pétalo

### Referencias en cada sección
Todas las secciones del informe incluyen un box de referencias bibliográficas.

### Link oficial Mason (2025)
Único link disponible: `https://drive.google.com/file/d/1nkjTOoW-4HUCbazcqPH-5G2ZsV2IosBB/view?usp=sharing`
Sin mencionar "Google Drive" — se trata como publicación oficial.

## Cambios v7.0

### Nuevos indicadores: ERP y HRP
- **🌍 ERP (Estado Regenerativo Presente)**: 80% MFP observado + 20% sub-indicadores M2-6
- **🌱 HRP (Horizonte Regenerativo Potencial)**: 100% MFP proyectado (obs+pot)
- **🌀 Brecha (HRP − ERP)**: Campo de acción con valor numérico + descripción dinámica

### Escala 0-10 con 5 niveles narrativos
| Rango | Nivel | Descripción |
|-------|-------|-------------|
| 0-2 | Sin inicio | El camino regenerativo está por comenzar |
| 2-4 | Semilla | Primeras prácticas activas |
| 4-6 | Brote | Prácticas en marcha, el espacio crece |
| 6-8 | Crecimiento | Prácticas consolidadas, regenera con fuerza |
| 8-10 | Abundancia | Referente vivo de regeneración |

## Stack
- Streamlit · Plotly · Supabase · Folium · python-docx · openpyxl

## Instalación
```bash
pip install -r requirements.txt
streamlit run app.py
```
