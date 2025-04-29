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
    "CAPR CALETA LAS PEÑAS",
    "CAPR CALETA TUBUL",
    "CAPR RUMENA",
    "CAPR HUENTELOLÉN",
    "CAPR HUILLINCO",
    "CAPR CAYUCUPIL",
    "CAPR PUNTA LAVAPIÉ",
    "CAPR HORCONES",
    "CAPR PICHILO",
    "CAPR DE COLLICO",
    "CAPR LLICO",
    "CAPR LARAQUETE - EL PINAR"
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
        resumen = df.groupby("Nombre SSR").mean()
        resumen["% Completado"] = resumen.mean(axis=1) * 100

        st.subheader("Resumen por SSR")
        st.dataframe(resumen[["% Completado"]].sort_values("% Completado", ascending=False))

        ssr_seleccionado = st.selectbox("Ver detalle de un SSR", options=df["Nombre SSR"].unique())
        if ssr_seleccionado:
            st.subheader(f"Detalle Checklist: {ssr_seleccionado}")
            detalle = df[df["Nombre SSR"] == ssr_seleccionado].iloc[-1]
            for item in checklist_items:
                st.write(f"{item}: {'✅' if detalle[item] else '❌'}")
