from fpdf import FPDF
from io import BytesIO
import os

def renglon(pdf, texto, valor):
    """Dibuja una línea de texto a la izquierda y su valor alineado a la derecha."""
    pdf.cell(120, 9, texto, ln=0)
    pdf.cell(0, 9, valor, align="R", ln=1)

def armar_pdf(nombre_negocio, rubro, numero, cliente, nombres, cantidades,
              precios_unitarios, subtotal, descuento, iva, total,
              forma_pago, logo_path="logo.png"):
    
    # 1. Creamos la hoja PDF
    pdf = FPDF()
    pdf.add_page()
    
    # 2. Ruta absoluta del logo para evitar fallos
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_logo = os.path.join(directorio_actual, logo_path)
    
    if os.path.exists(ruta_logo):
        pdf.image(ruta_logo, x=10, y=10, w=28)
        pdf.set_xy(40, 12)
    else:
        pdf.set_xy(10, 12)

    # 3. Encabezado
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, nombre_negocio, ln=1)
    
    if os.path.exists(ruta_logo):
        pdf.set_x(40)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, rubro, ln=1)
    pdf.ln(10)

    # 4. Datos del presupuesto
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "PRESUPUESTO", ln=1, align="C")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, f"Nro.: {numero}", ln=1)
    pdf.cell(0, 7, f"Cliente: {cliente}", ln=1)
    pdf.cell(0, 7, f"Forma de pago: {forma_pago}", ln=1)
    pdf.ln(5)

    # 5. Detalle de productos
    pdf.set_font("Helvetica", "", 11)
    for cantidad, nombre, precio in zip(cantidades, nombres, precios_unitarios):
        importe_renglon = cantidad * precio
        renglon(pdf, f"{cantidad} x {nombre}", f"$ {importe_renglon:,.2f} c/u")

    pdf.ln(5)

    # 6. Resumen de importes
    renglon(pdf, "Subtotal", f"$ {subtotal:,.2f}")
    renglon(pdf, "Descuento", f"- $ {descuento:,.2f}")
    renglon(pdf, "IVA (21%)", f"$ {iva:,.2f}")

    # 7. TOTAL en negrita
    pdf.set_font("Helvetica", "B", 13)
    renglon(pdf, "TOTAL", f"$ {total:,.2f}")

    # 8. Pie de página
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "Gracias por elegirnos. Presupuesto valido por 7 dias.", ln=1)

    # 9. SALIDA SEGURA CON BYTESIO (Solución definitiva para Streamlit y FPDF)
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        pdf_bytes = pdf_output.encode("latin-1")
    else:
        pdf_bytes = bytes(pdf_output)
        
    return pdf_bytes

# Alias obligatorio para compatibilidad con app.py
generar_pdf = armar_pdf
