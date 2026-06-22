import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

@st.cache_data
def load_data():
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_base, 'data', 'dataset_limpio.csv')
    return pd.read_csv(ruta_csv)

df = load_data()

df = load_data()

# 1. Traducir las temporadas (esto ya lo teníamos)
traducir_temporadas = {
    'Summer': 'Verano',
    'Winter': 'Invierno',
    'Spring': 'Primavera',
    'Fall': 'Otoño'
}
df['season'] = df['season'].replace(traducir_temporadas)

# 2. NUEVO: Traducir las categorías de ropa al español
traducir_categorias = {
    'Accessories': 'Accesorios',
    'Tops': 'Partes Superiores',
    'Bottoms': 'Partes Inferiores',
    'Outerwear': 'Ropa de Abrigo',
    'Dresses': 'Vestidos',
    'Footwear': 'Calzado',
    'Shoes': 'Calzado',
    'Activewear': 'Ropa Deportiva',
    'Swimwear': 'Trajes de Baño',
    'Intimates': 'Ropa Interior',
    'Lingerie': 'Lencería',
    'Jewelry': 'Joyería'
}
# Usamos .replace() para que, si hay una categoría en inglés que no pusimos en la lista, no se borre
df['category'] = df['category'].replace(traducir_categorias)

# --- ENCABEZADO ---
# (El resto del código sigue exactamente igual hacia abajo...)

# Traducir los valores de las temporadas para que se vean correctos en el gráfico
traducir_temporadas = {
    'Summer': 'Verano',
    'Winter': 'Invierno',
    'Spring': 'Primavera',
    'Fall': 'Otoño'
}
df['season'] = df['season'].map(traducir_temporadas).fillna(df['season'])

# --- ENCABEZADO ---
st.title("Análisis de E-Commerce de prendas de ropa")
st.markdown("""
**Pregunta de análisis:** ¿En qué categorías el descuento genera un mejor retorno neto (mayor ingreso, menor devolución y mejor calificación), y en cuáles deteriora la rentabilidad sin mejorar la satisfacción del cliente?

Este panel evalúa el **Ingreso Neto Real** retenido por la tienda, penalizando aquellas transacciones que terminaron en devolución.
""")

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros Interactivos")
st.sidebar.markdown("*Modifica los filtros para actualizar los gráficos en tiempo real.*")

temporada_sel = st.sidebar.multiselect(
    "1. Seleccionar Temporada", 
    df['season'].unique(), 
    default=df['season'].unique()
)

categoria_sel = st.sidebar.multiselect(
    "2. Seleccionar Categoría", 
    df['category'].unique(), 
    default=df['category'].unique()
)

min_desc, max_desc = float(df['markdown_percentage'].min()), float(df['markdown_percentage'].max())
rango_descuento = st.sidebar.slider(
    "3. Rango de Descuento (%)",
    min_value=min_desc, max_value=max_desc, value=(min_desc, max_desc)
)

# Aplicar filtros
df_filtrado = df[
    (df['season'].isin(temporada_sel)) &
    (df['category'].isin(categoria_sel)) & 
    (df['markdown_percentage'] >= rango_descuento[0]) & 
    (df['markdown_percentage'] <= rango_descuento[1])
]

# --- SECCIÓN: MÉTRICAS ---
st.subheader("Indicadores Globales de Rendimiento")
col1, col2, col3 = st.columns(3)

ingreso_total = df_filtrado['ingreso_neto'].sum()
tasa_dev = df_filtrado['devuelto_num'].mean() * 100
rating_prom = df_filtrado['customer_rating'].mean()

col1.metric("Ingreso Neto Real", f"${ingreso_total:,.0f}", help="Ingresos totales descontando los productos devueltos.")
col2.metric("Tasa de Devolución", f"{tasa_dev:.1f}%", help="Porcentaje de productos vendidos que fueron devueltos.")
col3.metric("Calificación Promedio", f"{rating_prom:.1f} / 5.0", help="Satisfacción promedio del cliente.")

st.divider()

# --- GRÁFICO 1: EL QUE TE GUSTABA (CORREGIDO A ESPAÑOL) ---
st.subheader("1. Ventas Netas: ¿Qué se vende más en cada temporada?")
st.markdown("*Ingreso neto real desglosado por temporada y categoría de prenda.*")

df_temporada = df_filtrado.groupby(['season', 'category'])['ingreso_neto'].sum().reset_index()

# Usamos 'labels' para cambiar los nombres de los campos técnicos a español en el gráfico
fig1 = px.bar(df_temporada, x='season', y='ingreso_neto', color='category', barmode='group',
              labels={
                  'season': 'Temporada', 
                  'ingreso_neto': 'Ingreso Neto Real ($)', 
                  'category': 'Categoría'
              })
st.plotly_chart(fig1, use_container_width=True)

st.info("💡 **Insight Comercial:** Este gráfico permite identificar qué colecciones generan el verdadero flujo de caja en cada estación del año.")

st.divider()

# --- SECCIÓN: GRÁFICO 2 Y TABLA (LEGIBLES Y EN ESPAÑOL) ---
col_graf2, col_graf3 = st.columns(2)

with col_graf2:
    st.subheader("2. Top 10 Categorías Más Rentables")
    st.markdown("*Las 10 prendas específicas con mayor retención de ingresos.*")
    
    df_top10 = df_filtrado.groupby('category')['ingreso_neto'].sum().reset_index()
    df_top10 = df_top10.sort_values('ingreso_neto', ascending=False).head(10)
    
    fig2 = px.bar(df_top10, x='ingreso_neto', y='category', orientation='h',
                  labels={
                      'category': 'Categoría', 
                      'ingreso_neto': 'Ingreso Neto ($)'
                  })
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

with col_graf3:
    st.subheader("3. Datos en Bruto: Rendimiento Detallado")
    st.markdown("*Tabla interactiva ordenable para analizar riesgos de devoluciones.*")
    
    df_tabla = df_filtrado.groupby('category').agg({
        'ingreso_neto': 'sum',
        'devuelto_num': 'mean',
        'customer_rating': 'mean'
    }).reset_index()
    
    # Renombrar y dar formato estético a las columnas de la tabla
    df_tabla['Tasa Devolución'] = (df_tabla['devuelto_num'] * 100).round(1).astype(str) + '%'
    df_tabla['Calificación'] = df_tabla['customer_rating'].round(1)
    df_tabla['Ingreso Neto ($)'] = df_tabla['ingreso_neto'].round(0)
    
    df_mostrar = df_tabla[['category', 'Ingreso Neto ($)', 'Tasa Devolución', 'Calificación']]
    df_mostrar.columns = ['Categoría', 'Ingreso Neto ($)', 'Tasa Devolución', 'Calificación']
    df_mostrar = df_mostrar.sort_values('Ingreso Neto ($)', ascending=False)
    
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
    st.success("✅ **Tip para la presentación:** Haz clic en el encabezado 'Tasa Devolución' para mostrarle a los profesores cuáles prendas fallan más.")