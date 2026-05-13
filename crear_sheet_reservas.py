#!/usr/bin/env python3
"""
CARWAS M&C 173 — Crear Google Sheet de Reservas
================================================
Crea automáticamente la hoja de cálculo con las columnas
correctas, formato y validaciones para el sistema de reservas.

REQUISITOS:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

CONFIGURAR ANTES DE EJECUTAR:
    1. Ir a https://console.cloud.google.com
    2. Crear proyecto → Activar "Google Sheets API" y "Google Drive API"
    3. Crear credenciales → "OAuth 2.0 Client ID" → "Desktop app"
    4. Descargar el JSON y renombrarlo a: credentials.json
    5. Poner credentials.json en la misma carpeta que este script
    6. Ejecutar: python3 crear_sheet_reservas.py

El script creará la hoja y mostrará el ID que usarás en n8n.
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Permisos necesarios
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Colores para el formato
COLOR_HEADER     = {"red": 0.063, "green": 0.063, "blue": 0.063}   # #0a0a0a
COLOR_HEADER_TXT = {"red": 0.961, "green": 0.773, "blue": 0.094}   # #f5c518 amarillo
COLOR_PENDIENTE  = {"red": 1.0,   "green": 0.953, "blue": 0.502}   # amarillo claro
COLOR_CONFIRMADO = {"red": 0.714, "green": 0.929, "blue": 0.745}   # verde claro
COLOR_COMPLETADO = {"red": 0.878, "green": 0.878, "blue": 0.878}   # gris
COLOR_CANCELADO  = {"red": 0.957, "green": 0.714, "blue": 0.714}   # rojo claro

COLUMNAS = [
    "Timestamp",
    "Fecha_Hora_CR",
    "Nombre",
    "Telefono",
    "Direccion",
    "Vehiculo",
    "Servicio",
    "Fecha_Servicio",
    "Hora_Preferida",
    "Precio",
    "Estado",
    "Notas"
]

ANCHOS_COLUMNA = [180, 160, 150, 120, 250, 130, 200, 130, 120, 100, 120, 200]


def autenticar():
    """Autenticar con Google OAuth2."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("❌ ERROR: No se encontró credentials.json")
                print("   Descargalo desde Google Cloud Console:")
                print("   https://console.cloud.google.com → APIs → Credenciales → OAuth 2.0")
                exit(1)
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())

    return creds


def crear_spreadsheet(service):
    """Crear el Google Sheet con todas las hojas necesarias."""
    spreadsheet = {
        'properties': {
            'title': 'Carwas M&C 173 — Sistema de Reservas',
            'locale': 'es_CR',
            'timeZone': 'America/Costa_Rica'
        },
        'sheets': [
            {'properties': {'title': 'Reservas',     'index': 0, 'sheetId': 1}},
            {'properties': {'title': 'Dashboard',    'index': 1, 'sheetId': 2}},
            {'properties': {'title': 'Configuracion','index': 2, 'sheetId': 3}},
        ]
    }
    result = service.spreadsheets().create(body=spreadsheet).execute()
    return result['spreadsheetId'], result['sheets']


def formatear_hoja_reservas(service, sheet_id):
    """Aplicar formato a la hoja Reservas."""
    requests = []

    # 1. Encabezados en fila 1
    requests.append({
        "updateCells": {
            "range": {
                "sheetId": 1,
                "startRowIndex": 0, "endRowIndex": 1,
                "startColumnIndex": 0, "endColumnIndex": len(COLUMNAS)
            },
            "rows": [{
                "values": [
                    {
                        "userEnteredValue": {"stringValue": col},
                        "userEnteredFormat": {
                            "backgroundColor": COLOR_HEADER,
                            "textFormat": {
                                "foregroundColor": COLOR_HEADER_TXT,
                                "bold": True,
                                "fontSize": 10,
                                "fontFamily": "Arial"
                            },
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "wrapStrategy": "WRAP"
                        }
                    }
                    for col in COLUMNAS
                ]
            }],
            "fields": "userEnteredValue,userEnteredFormat"
        }
    })

    # 2. Altura de fila de encabezados
    requests.append({
        "updateDimensionProperties": {
            "range": {"sheetId": 1, "dimension": "ROWS", "startIndex": 0, "endIndex": 1},
            "properties": {"pixelSize": 40},
            "fields": "pixelSize"
        }
    })

    # 3. Anchos de columnas
    for i, ancho in enumerate(ANCHOS_COLUMNA):
        requests.append({
            "updateDimensionProperties": {
                "range": {"sheetId": 1, "dimension": "COLUMNS", "startIndex": i, "endIndex": i+1},
                "properties": {"pixelSize": ancho},
                "fields": "pixelSize"
            }
        })

    # 4. Congelar primera fila
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": 1,
                "gridProperties": {"frozenRowCount": 1}
            },
            "fields": "gridProperties.frozenRowCount"
        }
    })

    # 5. Validación de datos en columna "Estado" (columna K = índice 10)
    requests.append({
        "setDataValidation": {
            "range": {
                "sheetId": 1,
                "startRowIndex": 1, "endRowIndex": 1000,
                "startColumnIndex": 10, "endColumnIndex": 11
            },
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [
                        {"userEnteredValue": "Pendiente"},
                        {"userEnteredValue": "Confirmado"},
                        {"userEnteredValue": "Completado"},
                        {"userEnteredValue": "Cancelado"}
                    ]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    })

    # 6. Formato de la columna Precio como moneda (₡)
    requests.append({
        "repeatCell": {
            "range": {
                "sheetId": 1,
                "startRowIndex": 1, "endRowIndex": 1000,
                "startColumnIndex": 9, "endColumnIndex": 10
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "CURRENCY",
                        "pattern": '"₡"#,##0'
                    }
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    })

    # 7. Bordes en toda la tabla
    requests.append({
        "updateBorders": {
            "range": {
                "sheetId": 1,
                "startRowIndex": 0, "endRowIndex": 500,
                "startColumnIndex": 0, "endColumnIndex": len(COLUMNAS)
            },
            "innerHorizontal": {
                "style": "SOLID",
                "color": {"red": 0.85, "green": 0.85, "blue": 0.85}
            },
            "innerVertical": {
                "style": "SOLID",
                "color": {"red": 0.85, "green": 0.85, "blue": 0.85}
            }
        }
    })

    return requests


def agregar_datos_config(service, sheet_id):
    """Agregar datos de configuración del negocio."""
    valores_config = [
        ["PARÁMETRO", "VALOR"],
        ["Negocio", "Carwas M&C 173"],
        ["Propietario", "Greivin"],
        ["WhatsApp", "8737-5227"],
        ["SINPE Móvil", "6094-5354"],
        ["Horario apertura", "06:00"],
        ["Horario cierre", "17:00"],
        ["Día libre", "Miércoles"],
        ["Anticipación mínima (horas)", "24"],
        ["", ""],
        ["PRECIOS", ""],
        ["Lavado básico - Auto 4x2", "5000"],
        ["Lavado básico - SUV/4x4", "7000"],
        ["Lavado + Encerado - Auto 4x2", "7000"],
        ["Lavado + Encerado - SUV/4x4", "10000"],
        ["Detallado completo (todos)", "25000"],
        ["", ""],
        ["ZONAS DE COBERTURA", ""],
        ["Zona 1", "Cartago Centro"],
        ["Zona 2", "Paraíso"],
        ["Zona 3", "Orosí"],
        ["Zona 4", "Cervantes"],
        ["Zona 5", "Dulce Nombre"],
        ["Zona 6", "Aguacaliente"],
    ]

    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Configuracion!A1",
        valueInputOption="RAW",
        body={"values": valores_config}
    ).execute()


def agregar_dashboard(service, sheet_id):
    """Agregar fórmulas de dashboard básico."""
    valores_dashboard = [
        ["📊 DASHBOARD — CARWAS M&C 173", "", "", ""],
        ["", "", "", ""],
        ["RESUMEN GENERAL", "", "", ""],
        ["Total reservas", "=COUNTA(Reservas!C2:C1000)", "", ""],
        ["Pendientes", "=COUNTIF(Reservas!K2:K1000,\"Pendiente\")", "", ""],
        ["Confirmadas", "=COUNTIF(Reservas!K2:K1000,\"Confirmado\")", "", ""],
        ["Completadas", "=COUNTIF(Reservas!K2:K1000,\"Completado\")", "", ""],
        ["Canceladas", "=COUNTIF(Reservas!K2:K1000,\"Cancelado\")", "", ""],
        ["", "", "", ""],
        ["INGRESOS", "", "", ""],
        ["Total ingresos completados", "=SUMIF(Reservas!K2:K1000,\"Completado\",Reservas!J2:J1000)", "", ""],
        ["Ingreso promedio por servicio", "=IFERROR(AVERAGEIF(Reservas!K2:K1000,\"Completado\",Reservas!J2:J1000),0)", "", ""],
        ["", "", "", ""],
        ["SERVICIOS MÁS POPULARES", "", "", ""],
        ["Lavado básico", "=COUNTIF(Reservas!G2:G1000,\"*básico*\")", "", ""],
        ["Lavado + Encerado", "=COUNTIF(Reservas!G2:G1000,\"*encerado*\")", "", ""],
        ["Detallado completo", "=COUNTIF(Reservas!G2:G1000,\"*Detallado*\")", "", ""],
        ["", "", "", ""],
        ["RESERVAS HOY", "", "", ""],
        ["=CONCATENATE(\"Citas para hoy (\",TEXT(TODAY(),\"DD/MM/YYYY\"),\")\")",
         "=COUNTIF(Reservas!H2:H1000,TEXT(TODAY(),\"YYYY-MM-DD\"))", "", ""],
    ]

    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="Dashboard!A1",
        valueInputOption="USER_ENTERED",
        body={"values": valores_dashboard}
    ).execute()


def main():
    print("")
    print("🚗 CARWAS M&C 173 — Crear Google Sheet de Reservas")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("")

    # Autenticar
    print("🔐 Autenticando con Google...")
    creds = autenticar()
    service = build('sheets', 'v4', credentials=creds)
    print("   ✅ Autenticado")

    # Crear spreadsheet
    print("")
    print("📊 Creando Google Sheet...")
    sheet_id, sheets = crear_spreadsheet(service)
    print(f"   ✅ Sheet creada con ID: {sheet_id}")

    # Formatear hoja Reservas
    print("")
    print("🎨 Aplicando formato a la hoja Reservas...")
    requests = formatear_hoja_reservas(service, sheet_id)
    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": requests}
    ).execute()
    print("   ✅ Formato aplicado")

    # Agregar configuración
    print("")
    print("⚙️  Agregando datos de configuración...")
    agregar_datos_config(service, sheet_id)
    print("   ✅ Configuración guardada")

    # Agregar dashboard
    print("")
    print("📈 Configurando dashboard...")
    agregar_dashboard(service, sheet_id)
    print("   ✅ Dashboard listo")

    # Guardar el ID para n8n
    config = {
        "google_sheet_id": sheet_id,
        "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}",
        "negocio": "Carwas M&C 173",
        "propietario": "Greivin"
    }
    with open('sheet_config.json', 'w') as f:
        json.dump(config, f, indent=2)

    print("")
    print("╔══════════════════════════════════════════════════════╗")
    print("║  ✅ ¡GOOGLE SHEET CREADO EXITOSAMENTE!              ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("")
    print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{sheet_id}")
    print("")
    print("📋 PRÓXIMOS PASOS:")
    print(f"   1. En n8n, buscar 'REEMPLAZAR_CON_ID_DE_TU_GOOGLE_SHEET'")
    print(f"      y reemplazar con: {sheet_id}")
    print("   2. Configurar credenciales de Google Sheets en n8n")
    print("   3. Importar el workflow n8n_workflow_carwas_mc.json")
    print("")
    print("💾 ID guardado en: sheet_config.json")
    print("")


if __name__ == "__main__":
    main()
