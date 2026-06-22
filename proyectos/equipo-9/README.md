# 👗 Análisis de Rentabilidad y Devoluciones en E-Commerce (Fashion Boutique 2025)

**Equipo 9** | Curso de Código y Programación - Samsung Innovation Campus Chile 2026
**Integrantes:** Seastian Toledo, Jeremy Marín, Benjamin Urra y Jairo Arias

---

## 📌 Acceso a la Aplicación
💻 **Dashboard Interactivo:** 

---

## 🎯 El Problema de Negocio (¿Por qué esta aplicación?)
En la industria del *retail* y el comercio electrónico de moda, medir el éxito basándose únicamente en el volumen de ventas brutas es una falacia financiera. Las tiendas suelen aplicar descuentos agresivos para rotar el inventario, pero estas estrategias a menudo generan "compras impulsivas". 

El resultado: el cliente se arrepiente, la prenda no cumple sus expectativas (baja satisfacción) y se devuelve el producto. Esto genera altos costos de logística inversa (envíos) y destruye el margen de ganancia. 

### 💡 Ejemplo de Uso Real en la Industria
Imagina a un Gerente de Finanzas o de Adquisiciones de una tienda retail. Se acerca la temporada de liquidación de verano y debe decidir a qué ropa aplicarle un 40% de descuento. 
Usando nuestro dashboard, el gerente filtra los datos y descubre que rebajar agresivamente la Ropa de Mujer dispara la tasa de devoluciones por encima del 50% y desploma la satisfacción del cliente a 2.8/5.0, perdiendo dinero neto. Sin embargo, en la categoría Hombres, el mismo descuento fideliza al cliente y retiene el efectivo en caja. Con esta información, el gerente redirige el presupuesto de marketing y cambia la política de precios, salvando la rentabilidad del trimestre.

---

## 📊 Pregunta de Análisis
> **¿Cómo impacta la temporada en el volumen de ventas netas, y en qué categorías las estrategias agresivas de descuento disparan las devoluciones y destruyen la rentabilidad real de la tienda?**

Para responder esto, creamos la métrica de **Ingreso Neto Real**: el dinero que efectivamente retiene la tienda, penalizando (llevando a $0) todas las transacciones que terminaron en una devolución.

---

## 🏗️ Estructura del Proyecto

El proyecto se divide en el desarrollo de 3 Notebooks analíticos y una Aplicación Web:

### 1. Notebooks (`/notebooks`)
* **`01_eda.ipynb` (Análisis Exploratorio):** Descomposición estructural del dataset. Analizamos las variables de negocio, distribución del inventario (stock nulo o negativo), revisión de registros sin tallas asignadas y rangos de fechas de operación.
* **`02_limpieza.ipynb` (Transformación):** Limpieza de nulos, traducción de categorías y temporadas al español para mejor visualización, y la creación de la lógica financiera del proyecto (`devuelto_num` e `ingreso_neto`).
* **`03_analisis.ipynb` (Análisis de Datos):** Cruce preliminar de las variables de rentabilidad, satisfacción y estacionalidad.

### 2. Dashboard Interactivo (`app.py`)
Desarrollado con **Streamlit** y **Plotly**, el panel cuenta con:
* **Filtros dinámicos:** Permiten segmentar la información en tiempo real por temporada, categoría de prenda y rango de descuento aplicado.
* **Indicadores Clave (KPIs):** Monitoreo directo del Ingreso Neto Real, la Tasa de Devolución y la Calificación Promedio del cliente.
* **Visualizaciones Ejecutivas:** * Gráfico de rentabilidad limpia por temporada.
    * Top 10 de categorías más rentables (Barras horizontales).
    * Tabla de datos en bruto ordenable con el detalle del riesgo de devolución.

---

## 🛠️ Tecnologías Utilizadas
* **Python 3.10+**
* **Pandas:** Manipulación y transformación de datos.
* **Plotly Express:** Visualizaciones interactivas de alto rendimiento.
* **Streamlit:** Despliegue de la aplicación web de ciencia de datos.
* **Git / GitHub:** Control de versiones.

---

## 🚀 Instrucciones de Ejecución Local

Si deseas correr esta aplicación en tu propia máquina:

1. Clona este repositorio y navega a la carpeta raíz (`sic_2026_c-p_cohort_1`).
2. Activa tu entorno virtual e instala las dependencias:
   ```bash
   pip install streamlit pandas plotly