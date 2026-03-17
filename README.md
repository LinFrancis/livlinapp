# 🌿 LivLin · Indagación Regenerativa v7.2

**Potencial para una vida regenerativa** · www.livlin.cl

## Cambios v7.2

### Tema visual fijo: Light
Archivo `.streamlit/config.toml` fuerza tema claro con colores LivLin.

### Contenido inclusivo
Se eliminaron referencias exclusivas a "urbano". La herramienta aplica a espacios urbanos, periurbanos y rurales.

### Perspectiva Comparada integrada
La pestaña "📊 Perspectiva Comparada" ahora integra todo el contenido de la Flor de la Permacultura:
- Radar dual ERP vs HRP
- Barras apiladas de 7 pétalos
- **Detalle pétalo a pétalo**: definición, ERP/HRP, interpretaciones, prácticas observadas y potenciales
- Sub-indicadores M2-6 con transparencia
- 10 Dimensiones con definiciones y barras
- Metodología de cálculo
- Mensaje motivacional con acompañamiento LivLin

### Narrativa explicativa completa
Cada indicador (ERP, HRP, Brecha) tiene definición clara. Escala de niveles con colores. Interpretación personalizada del resultado. Referencias cruzadas a secciones del informe.

### Fix: text_area height
Corregido `height=60` → `height=68` (mínimo requerido por Streamlit).

### Fix: sidebar keys
Todas las keys de `app.py` con prefijo `admin_*`. Sin posibilidad de colisión con keys de `report.py` (`rpt_*`).

## Stack
Streamlit · Plotly · Supabase · Folium · python-docx · openpyxl

## Instalación
```bash
pip install -r requirements.txt
streamlit run app.py
```
