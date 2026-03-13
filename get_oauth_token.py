#!/usr/bin/env python3
"""
Script de configuración OAuth para LivLin — Indagación Regenerativa
Ejecuta esto UNA VEZ en tu computador local para obtener el refresh_token
que luego pegas en los secrets de Streamlit Cloud.

USO:
  pip install google-auth-oauthlib google-api-python-client
  python get_oauth_token.py
"""
import json
import sys

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("\n❌ Falta instalar las librerías. Ejecuta:\n")
    print("   pip install google-auth-oauthlib google-api-python-client\n")
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/drive"]

print("\n" + "="*60)
print("  LivLin — Configuración OAuth de Google Drive")
print("="*60)
print("""
Antes de continuar necesitas:

1. Ir a console.cloud.google.com
2. Seleccionar tu proyecto 'livlinapp'
3. APIs y Servicios → Credenciales
4. + Crear credenciales → ID de cliente OAuth 2.0
5. Tipo de aplicación: 'Aplicación de escritorio'
6. Nombre: 'LivLin OAuth'
7. Descargar el JSON de credenciales
8. Pegar el contenido aquí cuando se pida
""")

print("Pega el contenido completo del JSON OAuth descargado")
print("(el archivo que empieza con {\"installed\":{...}})")
print("y presiona Enter dos veces cuando termines:\n")

lines = []
try:
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
except EOFError:
    pass

raw = "\n".join(lines).strip()

# Try to find the JSON even if user pasted extra text
import re
match = re.search(r'\{.*\}', raw, re.DOTALL)
if not match:
    print("\n❌ No se encontró JSON válido. Asegúrate de pegar el contenido completo.")
    sys.exit(1)

try:
    client_config = json.loads(match.group(0))
except json.JSONDecodeError as e:
    print(f"\n❌ JSON inválido: {e}")
    sys.exit(1)

# Validate it's the right type
if "installed" not in client_config and "web" not in client_config:
    print("\n❌ Este no parece ser un archivo OAuth 2.0 de aplicación de escritorio.")
    print("Asegúrate de elegir 'Aplicación de escritorio' al crear las credenciales.")
    sys.exit(1)

print("\n✅ JSON leído correctamente.")
print("\nAbriendo navegador para autorizar acceso a Google Drive...")
print("(Inicia sesión con la cuenta de Google que tiene la carpeta de LivLin)\n")

try:
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
except Exception as e:
    print(f"\n❌ Error en el flujo OAuth: {e}")
    print("\nAlternativa: usa run_console si no tienes navegador:")
    try:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_console()
    except Exception as e2:
        print(f"❌ También falló: {e2}")
        sys.exit(1)

print("\n✅ Autorización concedida.\n")

# Test the connection
try:
    service = build("drive", "v3", credentials=creds)
    about   = service.about().get(fields="user,storageQuota").execute()
    user    = about.get("user", {})
    quota   = about.get("storageQuota", {})
    used    = int(quota.get("usage", 0)) / (1024**3)
    total   = int(quota.get("limit", 0)) / (1024**3)
    print(f"  Cuenta: {user.get('emailAddress')}")
    print(f"  Cuota:  {used:.2f} GB usados / {total:.0f} GB total")
except Exception as e:
    print(f"  (No se pudo verificar cuota: {e})")

# Extract the key values
key = "installed" if "installed" in client_config else "web"
client_id     = client_config[key]["client_id"]
client_secret = client_config[key]["client_secret"]
refresh_token = creds.refresh_token

print("\n" + "="*60)
print("  ✅ COPIA ESTO en Streamlit Cloud → Settings → Secrets")
print("="*60)
print()

secrets_toml = f"""[gdrive]
enabled = true
folder_id = "PEGA_AQUI_EL_ID_DE_TU_CARPETA_EN_DRIVE"
auth_type = "oauth"

[gdrive.oauth]
client_id = "{client_id}"
client_secret = "{client_secret}"
refresh_token = "{refresh_token}"
token_uri = "https://oauth2.googleapis.com/token"
"""

print(secrets_toml)
print("="*60)
print("""
PASOS FINALES:
1. Copia el bloque de arriba
2. Reemplaza PEGA_AQUI_EL_ID_DE_TU_CARPETA_EN_DRIVE con el ID de tu carpeta
   (lo encuentras en la URL de la carpeta en Drive)
3. En Streamlit Cloud → tu app → Settings → Secrets → pega todo
4. Guarda → la app se reinicia → ya debería funcionar

IMPORTANTE: El refresh_token no expira. Si en el futuro necesitas regenerarlo,
simplemente ejecuta este script de nuevo.
""")

# Also save locally for reference
try:
    with open("oauth_secrets.toml", "w") as f:
        f.write(secrets_toml)
    print("💾 También guardado en oauth_secrets.toml (NO subas este archivo a GitHub)")
except Exception:
    pass
