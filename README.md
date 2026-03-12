# Indagación Regenerativa — LivLin

Instrumento de diagnóstico colectivo para espacios en transición regenerativa.

## Instalación y uso

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Logo
Reemplaza `assets/logolivlin.png` con el logo oficial de LivLin.

## Google Drive (opcional)
1. Crea un proyecto en [console.cloud.google.com](https://console.cloud.google.com)
2. Activa la API de Google Drive
3. Crea una cuenta de servicio y descarga el JSON de credenciales
4. Renómbralo `gdrive_sa.json` y colócalo en `credentials/`
5. Comparte tu carpeta de Drive con el email de la cuenta de servicio

## Geocodificación y clima
Usa Nominatim (OpenStreetMap) y Open-Meteo — sin API key.
Requiere conexión a internet al momento del diagnóstico.

## Estructura de módulos
- M1: Información del espacio + geolocalización + intención del grupo
- M2-3: Ecología del suelo, vegetación, fauna, flujos, cultivo
- M4-6: Contexto urbano, agua/energía, materiales/residuos
- M7-8: Flor de la Permacultura (7 pétalos) + Tao de la Regeneración
- M9: Síntesis, potenciales del sitio, plan de acción
- Informe Final: Dashboard + descarga Excel
