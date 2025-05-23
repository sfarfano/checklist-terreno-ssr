# checklist_ssr_app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import httpx
import io
from fpdf import FPDF

# --- Configuración Supabase REST API ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
SUPABASE_TABLE = "checklist_ssr"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}
# Lista fija de SSR integrada al código
lista_ssr = [
    "CAPR CALETA TUBUL",
    "CAPR CALETA LAS PEÑAS",
    "CAPR RUMENA",
    "CAPR HUENTELOLÉN",
    "CAPR HUILLINCO",
    "CAPR CAYUCUPIL",
    "CAPR PUNTA LAVAPIÉ",
    "CAPR HORCONES",
    "CAPR PICHILO",
    "CAPR DE COLLICO",
    "CAPR LLICO",
    "CAPR LARAQUETE -  EL PINAR",
    "RESP MUNI CAÑETE",
    "CAPR LA CURVA DE CAYUCUPIL",
    "CAPR PELECO",
    "CAPR LLENQUEHUE",
    "CAPR LLONCAO - PAICAVÍ",
    "CAPR LAUTARO ANTIQUINA",
    "CAPR PONOTRO",
    "CAPR CALEBU - ELICURA",
    "CAPR PELECO",
    "CAPR SAN JOSE DE COLICO",
    "CAPR PLEGARIAS",
    "CAPR PEHUÉN",
    "CAPR PICHARAUCO",
    "CAPR SANTA ROSA",
    "CAPR ISLA MOCHA",
    "CAPR TEMUCO CHICO",
    "CAPR SARA DE LEBU",
    "CAPR DE PANGUE",
    "CAPR QUIDICO",
    "CAPR VILLA LOS RIOS",
    "CAPR TIRÚA",
    "CAPR TRANAQUEPE",
    "CAPR DE RALCO",
    "SAN RAMON",
    "CAPR AGUA Y SOL",
    "CAPR LOS CANELOS",
    "CAPR CHILLANCITO",
    "CAPR SECTOR CHARRRUA",
    "CAPR VILLA PELUCA",
    "CAPR MARRIHUE",
    "CAPR SECTOR QUINEL",
    "CAPR LAGUNA COIHUICO",
    "CAPR EL PROGRESO",
    "CAPR SALTO DEL LAJA",
    "CAPR LOMAS DE ANGOL",
    "CAPR LA QUINTA PONIENTE",
    "CAPR SECTOR NOGALES DE MEMBRILLAR",
    "CAPR PUENTES NEGROS",
    "CAPR COLICHEU",
    "CAPR LOS LEONES",
    "CAPR LAS PLAYAS",
    "CAPR VIOLETA PARRA",
    "CAPR VILLA LAJA",
    "CAPR PUENTE PERALES",
    "AGUAS CRISTALINAS",
    "CHACAYAL NORTE Y SUR",
    "CACHAPOAL",
    "CERRO LA CRUZ DE LAJA",
    "LAS CIÉNAGAS",
    "LOS CIENOGOS",
    "BUENA VISTA DE LA COLONIA",
    "SANTA AMELIA",
    "CAPR SANTA ANA",
    "CAPR QUIYALLAL",
    "CAPR LOS CHIRRILLOS",
    "CAPR SANTA ELENA",
    "EL PERAL",
    "EL ALAMO",
    "MILLANTÚ",
    "LOS TRONCOS",
    "LAS ENCINAS",
    "SANTA FE",
    "NATRE RARINCO CENTRO Y SANTA CLARA",
    "SALTO DEL LAJA ORIENTE",
    "SAN CARLOS DE PUREN",
    "SALTO DEL LAJA",
    "PARAGUAY",
    "PATA DE GALLINA",
    "SAN LUIS SANTA LAURA",
    "LAS DELICIAS",
    "LA MONTAÑA",
    "VIRQUENCO",
    "CANTARRANA",
    "LLANO BLANCO PEJERREY",
    "SAN JOSE DE BIOBIO",
    "LA CAPILLA CERRO COLORADO",
    "VILLA DUQUECO",
    "SAN ANTONIO LAS QUINTAS",
    "PEÑAFLOR",
    "EL PINO SAN MIGUEL",
    "SECTOR DIUTO",
    "SANTA LUISA",
    "DICAHUE",
    "EL OLIVO",
    "LAS VEGAS",
    "AGUA PURA",
    "VILLA SAN FRANCISCO",
    "VILLA CACHAPOAL",
    "MESAMÁVIDA",
    "BELLAVISTA - LAS VIÑAS",
    "LOS ROBLES",
    "LA PERLA",
    "COIGUE",
    "MILLAPOA",
    "MALVÉN - SAN LUIS",
    "SANTA ADRIANA",
    "BUREO",
    "UNION LOS TILOS",
    "MUNILQUE IZAURIETA",
    "VILLA LA VICTORIA",
    "LUANCO",
    "RINCONADA DE TOLPAN",
    "VALLE LOS MAITENES RÍO HUALQUI",
    "EL AROMO 1",
    "VILLA LAS DELICIAS",
    "CORTE LIMA",
    "LAS GREDAS",
    "LA HUERTA",
    "MANZANARES",
    "EL CIPRÉS",
    "CAMPAMENTO",
    "MIRAFLORES",
    "SANTA AMELIA",
    "RIGUE",
    "CANTERAS",
    "AGUA PURA SAN RAMÓN",
    "RUCALHUE",
    "LONCOPANGUE",
    "EL HUACHI",
    "SAN LORENCITO",
    "BAJO DUQUECO",
    "VILLA MERCEDES",
    "LAS AGUILAS",
    "LOS JUNQUILLOS",
    "VILLUCURA",
    "LOS ALPES",
    "LOS AROMOS",
    "BAJO MININCO",
    "LOS NOTROS",
    "UNION AGUILA NIEVE",
    "LOS NARANJOS, LOS BOLDOS, MANIL BAJO",
    "TRUPAN",
    "LA AGUADA",
    "CERRO PARRA",
    "CAMBRALES",
    "ALTO RINCONADA BAJO",
    "COOPERATIVA POLCURA",
    "RERE",
    "OBRAS DE RIO CLARO",
    "PUENTE TAPIHUE-MISQUE",
    "CALETA CHOME",
    "QUILACOYA",
    "PUENTE PERALES",
    "CHAIMAVIDA SOTO",
    "CAMBRALES NORTE",
    "ANDALIÉN",
    "CANCHILLAS",
    "ISLA SANTA MARIA PUERTO SUR",
    "JUAN RIQUELME GARAY",
    "MONTERREY",
    "ISLA SANTA MARIA PUERTO NORTE",
    "COPIULEMU",
    "LOTATO",
    "PUENTE 5",
    "RIO CLARO",
    "TOMECO",
    "HUALLEREHUE",
    "UNIHUE",
    "TALCAMAVIDA",
    "SAUCE DE CARRIZAL",
    "LA GENERALA",
    "SONADORA DE PODUCO ALTO",
    "DIÑICO",
    "EL COIGUE SAN JORGE",
    "NUEVA ESPERANZA",
    "COLIUMO",
    "CALETA TUMBES",
    "ADELANTO PASO LARGO",
    "AGUAS CLARAS DE COLICO ALTO",
    "LAS CAMELIAS",
    "QUIEBRAFRENOS",
    "EL POLIGONO",
    "SANTA ROSA NEGRETE",
    "SANTA LAURA DE TUCUMAN",
    "SANTA ELENA Y VILLA FRANCISCO",
    "AGUAS CRISTALINAS",
    "AGUA DE LOS CAMPOS RAFAEL"
]

# Definición del checklist
checklist_items = [
    "¿Existe macromedidor operativo en el SSR?",
    "¿Se realizó campaña de medición de caudal ultrasónico?",
    "¿Se registraron horarios y resultados de las mediciones?",
    "¿Todo el personal utilizó EPP completo?",
    "¿Se llevaron todos los equipos obligatorios?",
    "¿Se levantaron elementos de producción, distribución, recolección y tratamiento?",
    "¿Se entregó información georreferenciada en GDB o SHP?",
    "¿Se realizó inspección visual de fugas y desgaste?",
    "¿Se verificó funcionamiento de los equipos principales?",
    "¿Se revisaron registros de análisis y mantenimiento?",
    "¿Se verificó volumen, altura, tapa y limpieza de estanques?",
    "¿Se evaluó estado de redes de agua potable (histórico de fallas)?",
    "¿Se revisaron equipos de la PTAS (bombas, válvulas, reactores)?",
    "¿Se registraron análisis de eficiencia de remoción?",
    "¿Se registraron caudales de entrada y salida de PTAS?",
    "¿Toda la información fue respaldada (fotos, coordenadas, mediciones)?",
    "¿Se registraron las tarifas aplicadas a los usuarios? (AP y AS)?",
    "¿Se registro si el SSR cuenta o no con telemetría?",
    "¿Se registro si el SSR cuenta o no con telemetríaSe levantaron puntos con GPS de toda la infraestructura? (incluidas posibles extensiones de red)?",
    "¿Se firmó acta de visita? (un acta por Sistema ya sea AP o AS)?",
    "¿Se consultaron procedimientos (retrolavado, hábitos de mantención, frecuencia toma de muestras, etc)?",
    "¿Se inspeccionó visualmente el agua tratada?",
    "¿Se midieron cámaras de PTAS para estimar capacidad?",
    "¿Se realizó test de jarra? (PTAS)?",
    "En caso de que no se realizara vuelo dron, ¿se georreferenciaron los vértices de cada recinto y se midieron los cercos?"
    
]
item_map = {f"item_{i+1}": item for i, item in enumerate(checklist_items)}

st.set_page_config(page_title="Checklist Terreno SSR", layout="centered")

# Botón global para limpiar selección
if st.sidebar.button("🔄 Limpiar selección"):
    for key in list(st.session_state.keys()):
        if key.startswith("ssr_") or key.endswith("_ssr_actual") or key.startswith("reg_") or key.startswith("edit_"):
            del st.session_state[key]
    st.experimental_rerun()
menu = st.sidebar.selectbox("Menú", ["Registro de Checklist", "Revisión de Avance", "Editar o Eliminar Registro"])

# --- Funciones REST ---
def insertar_registro(data):
    r = httpx.post(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}", headers=HEADERS, json=[data])
    return r.status_code == 201, r.text

def obtener_registros():
    r = httpx.get(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=*&order=fecha.desc", headers=HEADERS)
    return r.json() if r.status_code == 200 else []

def eliminar_registro(reg_id):
    httpx.delete(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{reg_id}", headers=HEADERS)

def actualizar_registro(reg_id, data):
    httpx.patch(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{reg_id}", headers=HEADERS, json=data)

# Persistencia global SSR seleccionado
if "ssr_revision" not in st.session_state:
    st.session_state.ssr_revision = ""
if "ssr_edicion" not in st.session_state:
    st.session_state.ssr_edicion = ""
if "ssr_registro" not in st.session_state:
    st.session_state.ssr_registro = ""

# --- Registro ---
if menu == "Registro de Checklist":
    st.title("✅ Registro de Checklist de Terreno")
    opciones = ["Selecciona un SSR..."] + lista_ssr
    if st.session_state.ssr_registro not in opciones:
        st.session_state.ssr_registro = "Selecciona un SSR..."
    nombre_ssr = st.selectbox("Selecciona el Nombre del SSR", opciones, key="ssr_registro")
    if nombre_ssr != "Selecciona un SSR...":
        # Limpiar los checkboxes si cambia el SSR seleccionado
        if "registro_ssr_actual" not in st.session_state or st.session_state.registro_ssr_actual != nombre_ssr:
            for i in range(len(checklist_items)):
                st.session_state.pop(f"reg_{i}", None)
            st.session_state.registro_ssr_actual = nombre_ssr

        respuestas = {f"item_{i+1}": st.checkbox(item, key=f"reg_{i}") for i, item in enumerate(checklist_items)}
        if st.button("Guardar Registro"):
            nuevo = {"fecha": datetime.now().isoformat(), "nombre_ssr": nombre_ssr}
            nuevo.update(respuestas)
            ok, resp = insertar_registro(nuevo)
            if ok:
                st.success("✅ Registro guardado exitosamente.")
                st.experimental_rerun()
            else:
                st.error(f"❌ Error al guardar: {resp}")

# --- Revisión ---
elif menu == "Revisión de Avance":
    st.title("📋 Revisión de Avance General")
    registros = obtener_registros()
    if not registros:
        st.warning("No hay registros disponibles aún.")
    else:
        df = pd.DataFrame(registros)
        columnas_check = [col for col in df.columns if col.startswith("item_")]
        resumen = df.groupby("nombre_ssr")[columnas_check].mean()
        resumen["% Completado"] = resumen.mean(axis=1) * 100
        st.subheader("Resumen por SSR")
        st.dataframe(resumen[["% Completado"]].sort_values("% Completado", ascending=False))

        if "revision_ssr_actual" not in st.session_state or st.session_state.revision_ssr_actual != st.session_state.ssr_revision:
            st.session_state.revision_ssr_actual = st.session_state.ssr_revision
        ssr_sel = st.selectbox("Ver detalle de un SSR", df["nombre_ssr"].unique(), key="ssr_revision")

        if ssr_sel:
            st.subheader(f"Detalle Checklist: {ssr_sel}")
            fila = df[df["nombre_ssr"] == ssr_sel].iloc[-1]
            for clave, item in item_map.items():
                st.write(f"{item}: {'✅' if fila[clave] else '❌'}")

# --- Edición o eliminación ---
elif menu == "Editar o Eliminar Registro":
    st.title("✏️ Editar o Eliminar Registro")
    registros = obtener_registros()
    if not registros:
        st.warning("No hay registros aún.")
    else:
        df = pd.DataFrame(registros)

        ssr_edit = st.selectbox("Selecciona un SSR", df["nombre_ssr"].unique(), key="ssr_edicion")
        registros = df[df["nombre_ssr"] == ssr_edit]
        if not registros.empty:
            ultimo = registros.iloc[-1]
            st.write("Último registro:")
            st.dataframe(pd.DataFrame([ultimo]))
            if st.button("❌ Eliminar este registro"):
                eliminar_registro(ultimo["id"])
                st.success("Registro eliminado correctamente.")
                st.experimental_rerun()
            if st.checkbox("✏️ Editar este registro"):
                if "edicion_ssr_actual" not in st.session_state or st.session_state.edicion_ssr_actual != ssr_edit:
                    for i in range(len(checklist_items)):
                        st.session_state.pop(f"edit_{i}", None)
                    st.session_state.edicion_ssr_actual = ssr_edit

                ediciones = {
                    f"item_{i+1}": st.checkbox(item, value=bool(ultimo[f"item_{i+1}"]), key=f"edit_{i}")
                    for i, item in enumerate(checklist_items)
                }
                if st.button("Guardar cambios"):
                    actualizar_registro(ultimo["id"], ediciones)
                    st.success("Cambios guardados correctamente.")
                    st.experimental_rerun()

# --- Exportación ---
st.sidebar.markdown("## 📥 Exportación de Informes")
registros = obtener_registros()
if registros:
    df = pd.DataFrame(registros)
    columnas_check = [col for col in df.columns if col.startswith("item_")]
    resumen = df.groupby("nombre_ssr")[columnas_check].mean()
    resumen["% Completado"] = resumen.mean(axis=1) * 100
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        resumen[["% Completado"]].to_excel(writer, sheet_name='Resumen')
        for ssr in df["nombre_ssr"].unique():
            df[df["nombre_ssr"] == ssr].to_excel(writer, sheet_name=ssr[:31], index=False)
    st.sidebar.download_button("📥 Descargar Excel completo", output.getvalue(), "checklist_detalle.xlsx")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Informe Completo Checklist SSR", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.ln(5)
    for ssr in resumen.index:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, f"{ssr} - {round(resumen.loc[ssr]['% Completado'], 1)}% Completado", ln=True)
        pdf.set_font("Arial", "", 10)
        registros = df[df["nombre_ssr"] == ssr]
        for idx, fila in registros.iterrows():
            pdf.cell(0, 6, f"Fecha: {fila['fecha']}", ln=True)
            for clave, item in item_map.items():
                valor = 'SI' if fila[clave] else 'NO'
                pdf.multi_cell(0, 5, f"{item}: {valor}")
            pdf.ln(3)
        pdf.ln(5)
    pdf_output = io.BytesIO(pdf.output(dest='S').encode('latin1', 'replace'))
    st.sidebar.download_button("📄 Descargar PDF completo", data=pdf_output, file_name="checklist_completo.pdf")
else:
    st.sidebar.warning("No hay registros para exportar.")
