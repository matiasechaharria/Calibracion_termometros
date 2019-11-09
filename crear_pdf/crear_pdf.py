#crea pdf con de los certificados
#https://www.blog.pythonlibrary.org/2018/06/05/creating-pdfs-with-pyfpdf-and-python/

#relatorio # tambien sirve para exportar en distintos formatos
from fpdf import FPDF, HTMLMixin
import datetime
import time


class HTML2PDF(FPDF, HTMLMixin):
    pass
class CustomPDF(FPDF):
    pass

#def export_certificado(equipos):
def export_certificado(temp,correccion,incertidumbre):
    now = datetime.datetime.now()
    nowAux = str(now)
    nombre_certificado = nowAux[0:20]

    pdf=FPDF(format='A4', unit='mm')
    pdf.add_page()

    pdf.set_font('Arial','',10.0)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4

    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.
    th = pdf.font_size
    pdf.set_font('Times','B',14.0)
    pdf.cell(epw, 0.0, '', align='C')
    pdf.set_font('Times','',10.0)
    pdf.ln(0.5)

    # Here we add more padding by passing 2*th as height
    pdf.cell(col_width, 2*th, str( nombre_certificado ), border=1)
    pdf.cell(col_width, 2*th, str( temp ), border=1)
    pdf.cell(col_width, 2*th, str( correccion ), border=1)
    pdf.cell(col_width, 2*th, str( incertidumbre ), border=1)

    name = "certificados/"+"Certificado_"+str(nombre_certificado)+".pdf"
    pdf.output(name)





def export_certificado2(temp,correccion,incertidumbre):
    pdf = HTML2PDF()
    now = datetime.datetime.now()
    nowAux = str(now)
    nombre_certificado = nowAux[0:10]
    print(temp)
    print(correccion)
    print(incertidumbre)
    table = '''
    <h1 align="center">CERTIFICADO DE CALIBRACION</h1>
    <table border="0" align="center" width="50%">
    <thead>
        <tr>
            <th width="30%">Temperatura</th>
            <th width="70%">Correccion</th>
            <th width="30%">Incertidumbre</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>cell 1</td><td>cell 2</td><td>cell 3</td></tr>
        <tr><td>cell 4</td><td>cell 5</td><td>cell 6</td></tr>
        <tr><td>cell 7</td><td>cell 7</td><td>cell 9</td></tr>
    </tbody>
    </table>
    '''

    pdf.add_page()
    pdf.write_html(table)
    name = str(nombre_certificado)+".pdf"
    pdf.output(name)

def Historico_pdf(spacing=1):
    now = datetime.datetime.now()
    nowAux = str(now)
    nombre_certificado = nowAux[0:10]

    # data = [['First Name', 'Last Name', 'email', 'zip'],
    #         ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
    #         ['John', 'Doe', 'jdoe@doe.com', '12345'],
    #         ['Nina', 'Ma', 'inane@where.com', '54321']
    #         ]

    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)

    name = str(nombre_certificado)+"Historico_sondas"+".pdf"
    pdf.output(name)


def simple_table(spacing=1):
    now = datetime.datetime.now()
    nowAux = str(now)
    nombre_certificado = nowAux[0:10]

    # data = [['First Name', 'Last Name', 'email', 'zip'],
    #         ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
    #         ['John', 'Doe', 'jdoe@doe.com', '12345'],
    #         ['Nina', 'Ma', 'inane@where.com', '54321']
    #         ]

    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height*spacing)

    name = str(nombre_certificado)+".pdf"
    pdf.output(name)

def Historico_pdf_2(data):
    pdf=FPDF(orientation = 'L',format='A4', unit='mm')

    pdf.add_page()

    pdf.set_font('Times','',10.0)

    # Effective page width, or just epw
    epw = pdf.w - 2*pdf.l_margin

    # Set column width to 1/4 of effective page width to distribute content
    # evenly across table and page
    col_width = epw/8

    pdf.set_font('Times','B',14.0)
    pdf.cell(epw, 0.0, 'Historico de sondas', align='C')
    pdf.set_font('Times','',10.0)
    pdf.ln(5)

    th = pdf.font_size

    pdf.cell(col_width, 2*th, "Equipo", border=1)
    pdf.cell(col_width, 2*th, "Sonda", border=1)
    pdf.cell(col_width, 2*th, "Medicion", border=1)
    pdf.cell(col_width, 2*th, "Certificados", border=1)
    pdf.cell(col_width, 2*th, "Temperatura", border=1)
    pdf.cell(col_width, 2*th, "Correccion", border=1)
    pdf.cell(col_width, 2*th, "Incertidumbre", border=1)
    pdf.ln(th)
    pdf.ln(th)

    for row in data:
        for datum in row:
            pdf.cell(col_width, th, str(datum), border=1)

        pdf.ln(th)

    now = datetime.datetime.now()
    nowAux = str(now)
    nombre_pdf = nowAux[0:20]

    name = "Historico_sondas/"+str(nombre_pdf)+"Historico_pdf_2"+".pdf"
    pdf.output(name)



if __name__ == '__main__':
    simple_table()
