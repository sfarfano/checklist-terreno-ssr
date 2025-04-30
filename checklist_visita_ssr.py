import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuraciones Iniciales
st.set_page_config(page_title="Checklist Terreno SSR", layout="centered")

# Archivos
archivo_datos = "checklist_terreno.csv"

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
    "¿Se entregó carta Gantt al IF con 2 semanas de anticipación?",
    "¿Se informó personal que asistirá a terreno (mínimo 2 profesionales)?",
    "¿El Gestor Social DOH aprobó primer contacto?",
    "¿Todo el personal utilizó EPP completo?",
    "¿Se llevaron todos los equipos obligatorios?",
    "¿Se levantaron elementos de producción, distribución, recolección y tratamiento?",
    "¿Se entregó información georreferenciada en GDB o SHP?",
    "¿Se llenó y entregó la planilla de metadatos (Anexo 10)?",
    "¿Se realizó inspección visual de fugas y desgaste?",
    "¿Se verificó funcionamiento de los equipos principales?",
    "¿Se revisaron registros de análisis y mantenimiento?",
    "¿Se verificó volumen, altura, tapa y limpieza de estanques?",
    "¿Se evaluó estado de redes de agua potable (histórico de fallas)?",
    "¿Se revisaron equipos de la PTAS (bombas, válvulas, reactores)?",
    "¿Se registraron análisis de eficiencia de remoción?",
    "¿Se registraron caudales de entrada y salida de PTAS?",
    "¿Toda la información fue respaldada (fotos, coordenadas, mediciones)?"
]

# Cargar datos existentes
if os.path.exists(archivo_datos):
    df = pd.read_csv(archivo_datos)
else:
    df = pd.DataFrame()

# Menú principal
menu = st.sidebar.selectbox("Menú", ["Registro de Checklist", "Revisión de Avance"])

if menu == "Registro de Checklist":
    st.title("✅ Registro de Checklist de Terreno")

    nombre_ssr = st.selectbox("Selecciona el Nombre del SSR", options=["Selecciona un SSR..."] + lista_ssr)

    if nombre_ssr != "Selecciona un SSR...":
        respuestas = {}
        st.subheader("Checklist de Actividades")
        for item in checklist_items:
            respuesta = st.checkbox(item)
            respuestas[item] = respuesta

        if st.button("Guardar Registro"):
            nuevo_registro = {"Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Nombre SSR": nombre_ssr}
            nuevo_registro.update(respuestas)

            df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
            df.to_csv(archivo_datos, index=False)
            st.success("✅ Registro guardado exitosamente!")

elif menu == "Revisión de Avance":
    st.title("📋 Revisión de Avance General")

    if df.empty:
        st.warning("No hay registros disponibles aún.")
    else:
        columnas_numericas = df.drop(columns=["Fecha"]).select_dtypes(include="number").columns
        resumen = df.groupby("Nombre SSR")[columnas_numericas].mean()
        resumen["% Completado"] = resumen.mean(axis=1) * 100

        st.subheader("Resumen por SSR")
        st.dataframe(resumen[["% Completado"]].sort_values("% Completado", ascending=False))

        ssr_seleccionado = st.selectbox("Ver detalle de un SSR", options=df["Nombre SSR"].unique())
        if ssr_seleccionado:
            st.subheader(f"Detalle Checklist: {ssr_seleccionado}")
            detalle = df[df["Nombre SSR"] == ssr_seleccionado].iloc[-1]
            for item in checklist_items:
                st.write(f"{item}: {'✅' if detalle[item] else '❌'}")
