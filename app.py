import streamlit as st
import mi_negocio
import calculos
import pdf_presupuesto

# 1. Configuración de la página
st.set_page_config(
    page_title=f"Presupuestos | {mi_negocio.NOMBRE_NEGOCIO}",
    page_icon="🧾",
    layout="centered"
)

# 2. Títulos y encabezado visibles
st.title(f"🧾 {mi_negocio.NOMBRE_NEGOCIO}")
st.caption(f"Calculadora de presupuestos · {mi_negocio.RUBRO}")
st.write("Elegí hasta tres productos, ingresá las cantidades y seleccioná la forma de pago.")

# 3. Entrada de datos con widgets permitidos
cliente = st.text_input("Nombre del cliente", placeholder="Ej: Juli")

RENGLONES = 3
nombres = []
cantidades = []
precios_unitarios = []

for i in range(RENGLONES):
    st.subheader(f"Renglón {i + 1}")
    producto = st.selectbox(
        f"Producto {i + 1}",
        mi_negocio.productos,
        key=f"producto_{i}"
    )
    cantidad = st.number_input(
        f"Cantidad {i + 1}",
        min_value=0,
        step=1,
        value=0,
        key=f"cantidad_{i}"
    )
    
    if cantidad > 0:
        pos = calculos.buscar_posicion(mi_negocio.productos, producto)
        if pos >= 0:
            nombres.append(producto)
            cantidades.append(int(cantidad))
            precios_unitarios.append(mi_negocio.precios[pos])

forma_pago = st.radio(
    "Forma de pago",
    [mi_negocio.EFECTIVO, mi_negocio.TRANSFERENCIA],
    horizontal=True
)

st.divider()

# 4. Lógica de validación, cálculos y visualización de resultados
if not nombres:
    st.warning("Elegí al menos un producto con cantidad mayor que 0 para generar el presupuesto.")
else:
    # Llamada a las funciones puras de calculos.py
    subtotal, descuento, iva, total = calculos.calcular_presupuesto(
        cantidades, precios_unitarios, forma_pago, mi_negocio.EFECTIVO
    )
    
    st.subheader("Resumen")
    st.metric("Subtotal", f"$ {subtotal:,.2f}")
    st.metric("Descuento", f"$ {descuento:,.2f}")
    st.metric("IVA (21%)", f"$ {iva:,.2f}")
    st.metric("TOTAL A PAGAR", f"$ {total:,.2f}")

    if not cliente.strip():
        st.warning("Ingresá el nombre del cliente para habilitar la descarga del PDF.")
    else:
        # Generación y descarga del PDF utilizando la estructura vista en clases
        pdf_bytes = pdf_presupuesto.generar_pdf(
            nombre_negocio=mi_negocio.NOMBRE_NEGOCIO,
            rubro=mi_negocio.RUBRO,
            numero=1,
            cliente=cliente.strip(),
            nombres=nombres,
            cantidades=cantidades,
            precios_unitarios=precios_unitarios,
            subtotal=subtotal,
            descuento=descuento,
            iva=iva,
            total=total,
            forma_pago=forma_pago,
            logo_path="logo.png"
        )
        
        st.download_button(
            label="📄 Descargar presupuesto PDF",
            data=pdf_bytes,
            file_name="presupuesto.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.divider()
st.caption("Los precios del catálogo son de ejemplo. Editá mi_negocio.py para usar tu propio negocio.")
