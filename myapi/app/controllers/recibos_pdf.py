import os
from fpdf import FPDF
from app import db 
from app.controllers.recibosVuelos import RecibosController
from app.models.user_model import Recibos
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
from app.models.user_model import UsuariosTienenRecibos
from app.models.user_model import Usuarios


class ReciboPDF(FPDF):
    
    def header(self):
        # Encabezado del PDF
        # Logo
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al logo en la carpeta raíz
        ruta_logo = os.path.join(directorio_actual, 'logo.png')

        self.image(ruta_logo,10,8,33)
        self.set_font('Arial', 'B''U', 12)
        self.cell(0, 10, 'Recibo Aeroclub Lincoln', 0, 1, 'C')

    def datos_recibo(self, data, fecha):
        # Información del recibo
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f"Fecha: {fecha}", 0, 1)
        self.cell(0, 10, f"- Asociado: {data['asociado']}", 0, 1)
        self.cell(0, 10, f"- Instructor: {data['instructor']}", 0, 1)
        self.cell(0, 10, f"- Gestor: {data['gestor']}", 0, 1)
        self.cell(0, 10, f" -Matrícula: {data['matricula']}", 0, 1)
        self.cell(0, 10, f"- Observaciones: {data['observaciones']}", 0, 1)
        self.cell(0, 10, "--------------------------------------------------------------------------------------------------", 0, 1)
        self.cell(0, 10, f"- Precio Total: {data['precioTotal']}", 0, 1)
        self.cell(0, 10, "--------------------------------------------------------------------------------------------------", 0, 1)
        self.cell(0, 10, '', 0, 1)

    def itinerarios(self, itinerarios):
        # Detalles de los itinerarios
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, 'Itinerarios', 0, 1)

        self.set_font('Arial', '', 10)
        for itinerario in itinerarios:
            self.cell(0, 10, f"Hora de Salida: {itinerario['horaSalida']}", 0, 1)
            self.cell(0, 10, f"Código Aero. Salida: {itinerario['codAeroSalida']}", 0, 1)
            self.cell(0, 10, f"Hora de Llegada: {itinerario['horaLlegada']}", 0, 1)
            self.cell(0, 10, f"Código Aero. Llegada: {itinerario['codAeroLlegada']}", 0, 1)
            self.cell(0, 10, f"Cantidad de Aterrizajes: {itinerario['cantAterrizajes']}", 0, 1)
            self.cell(0, 10, f"Tipo de Itinerario: {itinerario['tipoItinerario']}", 0, 1)
            self.cell(0, 10, '', 0, 1)  # Espacio entre itinerarios

    def generar_nombre_archivo(self, id_recibos):
    
        return os.path.join(os.path.expanduser('~'), 'Descargas', f"recibo_{id_recibos}.pdf")  #guarda el pdf en descargas, verificar autorizacion. EL NOMRE ES EL ID DEL RECIBO.

    def crear_pdf (self,numRecibo):
    # Crear el objeto PDF
        pdf = ReciboPDF()
        pdf.add_page()

        try:
            recibosController = RecibosController()
            recibos = recibosController.obtenerUnRecibo(numRecibo)
            print(f"recibos: {recibos}")
             # Datos del recibo
             
            recibo = db.session.query(Recibos).filter_by(numero_recibos=numRecibo).first()
            user_tiene_recibo = db.session.query(UsuariosTienenRecibos).filter_by(rol="Asociado",recibos_id=recibo.id_recibos).first()
            id_asociado = user_tiene_recibo.usuarios_id
            asociado = db.session.query(Usuarios).filter_by(id_usuarios =id_asociado).first()
            emailAsociado = asociado.email
            fecha_recibo = recibo.fecha

            numRecibo = recibo.numero_recibos
            pdf.datos_recibo(recibos[0], fecha_recibo)
            recibos.pop(0)
            pdf.itinerarios(recibos)
            
        # Guardar el PDF con el nombre de archivo generado
            ##directorio_actual_normalizado = os.path.normpath(directorio_actual)
            namePdf = f'recibo-{numRecibo}.pdf'
            pdf.output(namePdf, 'F')
            print(f"El recibo ha sido creado como '{namePdf}'")

        #variables de entorno del email
         # Carga las variables de entorno desde el archivo .env
            load_dotenv()

                # Ahora puedes acceder a las variables de entorno como si estuvieran definidas en el sistema
            emailSmtp = os.getenv('EMAIL_SMTP')
            passwordSmtp = os.getenv('PASSWORD_SMTP')        

        # Envío por correo electrónico
            msg = EmailMessage()
            msg['Subject'] = 'Recibo'
            msg['From'] = emailSmtp  # Cambia esto al remitente real
            msg['To'] = emailAsociado # pasarle el emailAsociado correspondiente 
            msg.set_content(f'Adjunto encontrarás el recibo número {numRecibo}') #Mensaje del cuerpo de email

            numRecibo = recibo.numero_recibos

            with open(namePdf, 'rb') as f:   #Abre el archivo PDF en modo lectura binaria ('rb')
                contenido_pdf = f.read()    #Lee el contenido del archivo PDF y lo guarda en la variable contenido_pdf.
                nombre_pdf = os.path.basename(namePdf)   #Obtiene el nombre del archivo PDF sin la ruta completa.
                msg.add_attachment(contenido_pdf, maintype='application', subtype='octet-stream', filename=nombre_pdf)      #Adjunta el contenido del archivo PDF al correo electrónico utilizando el método add_attachment.

            # Configura el servidor SMTP y envía el correo
            servidor_smtp = 'smtp.gmail.com'  # Cambia esto según tu proveedor de correo
            puerto_smtp = 587  # Cambia el puerto si es diferente (puede ser 465)
            usuario_smtp = emailSmtp  # Cambia esto al correo real
            password_smtp = passwordSmtp  # Cambia esto a tu contraseña real

            try:

                with smtplib.SMTP(servidor_smtp, puerto_smtp) as servidor:
                    servidor.starttls()       # inicia una conexión segura con el servidor SMTP mediante el protocolo TLS (Transport Layer Security)
                    servidor.login(usuario_smtp, password_smtp)
                    servidor.send_message(msg)

                print(f"El recibo ha sido enviado por correo electrónico {emailAsociado}")
            except Exception as e:
                    print(f"Error al enviar el correo electrónico: {e}") 
            
            try:
                # Obtiene la ruta absoluta del archivo actual (script)
                ruta_actual = os.path.abspath(__file__)

                # Retrocede dos niveles para llegar a la "carpeta raíz" del proyecto
                ruta_pdf = os.path.abspath(os.path.join(ruta_actual, '..', '..', '..',f'../{nombre_pdf}'))
                os.remove(ruta_pdf)
                print(f"Archivo {ruta_pdf} eliminado exitosamente.")
            except FileNotFoundError:
                print(f"El archivo {ruta_pdf} no existe.")
            except Exception as e:
                print(f"Ocurrió un error al intentar borrar el archivo: {e}")
            
            return True
        
        except Exception as ex:
            print(ex)
            return  False
        