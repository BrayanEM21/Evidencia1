import csv
import datetime
import json
import os
import re
import openpyxl
from openpyxl.styles import Alignment


class Servicio:
    def __init__(self, nombre, costo):
        self.nombre = nombre
        self.costo = costo

class Nota:
    folio_counter = 1
    
    def __init__(self, cliente):
        self.folio = Nota.folio_counter
        Nota.folio_counter += 1
        self.fecha_inicio = None
        self.fecha_fin = None
        self.cliente = cliente
        self.rfc = None
        self.correo = None
        self.cancelada = False
        self.servicios = []

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
    
    def calcular_total(self):
        total = sum(servicio.costo for servicio in self.servicios)
        return round(total, 2)
    
patron_rfc_oficial = r'^[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]$'
patron_rfc_reducido = r'^[A-Za-zñÑ&]{3,4}\d{6}\w{3}$'
patron_rfc_personalizado = r'^(((?!(([CcKk][Aa][CcKkGg][AaOo])|([Bb][Uu][Ee][YyIi])|([Kk][Oo](([Gg][Ee])|([Jj][Oo])))|([Cc][Oo](([Gg][Ee])|([Jj][AaEeIiOo])))|([QqCcKk][Uu][Ll][Oo])|((([Ff][Ee])|([Jj][Oo])|([Pp][Uu]))[Tt][Oo])|([Rr][Uu][Ii][Nn])|([Gg][Uu][Ee][Yy])|((([Pp][Uu])|([Rr][Aa]))[Tt][Aa])|([Pp][Ee](([Dd][Oo])|([Dd][Aa])|([Nn][Ee])))|([Mm](([Aa][Mm][OoEe])|([Ee][Aa][SsRr])|([Ii][Oo][Nn])|([Uu][Ll][Aa])|([Ee][Oo][Nn])|([Oo][Cc][Oo])))))[A-Za-zñÑ&][aeiouAEIOUxX]?[A-Za-zñÑ&]{2}(((([02468][048])|([13579][26]))0229)|(\d{2})((02((0[1-9])|1\d|2[0-8]))|((((0[13456789])|1[012]))((0[1-9])|((1|2)\d)|30))|(((0[13578])|(1[02]))31)))[a-zA-Z1-9]{2}[\dAa])|([Xx][AaEe][Xx]{2}010101000))$'

patron_rfc_caracter_por_caracter = r'^[A-Za-zñÑ&]{1,2}([A-Za-zñÑ&]([A-Za-zñÑ&](\d(\d(\d(\d(\d(\d(\w(\w(\w)?)?)?)?)?)?)?)?)?)?)?$'

def validar_rfc(rfc):
    if re.match(patron_rfc_oficial, rfc) or re.match(patron_rfc_reducido, rfc) or re.match(patron_rfc_personalizado, rfc):
        return True
    else:
        return False
    

def fecha_actual():
    fecha_actual = datetime.datetime.now()
    return fecha_actual.strftime("%d-%m-%Y")  



def validar_correo(correo):
  
    patron_correo = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if re.match(patron_correo, correo):
        return True
    else:
        return False



def registrar_nota(notas):
    while True:
        try:
            cliente = input("Ingrese el nombre del cliente: ")

            if cliente.isdigit():
                raise ValueError("El nombre del cliente no puede ser un número.")
            if not cliente:
                raise ValueError("El nombre del cliente no puede estar vacío.")
            
            rfc = input("Ingrese el RFC del cliente: ").upper()
            if not rfc:
                print("El RFC del cliente no puede estar vacío. Intente nuevamente.")
                continue

            while not validar_rfc(rfc):
                print("RFC no válido. Intente nuevamente.")
                rfc = input("Ingrese el RFC del cliente: ").upper()

            correo = input("Ingrese el correo del cliente: ")
            if not correo:
                print("El correo del cliente no puede estar vacío. Intente nuevamente.")
                continue

            while not validar_correo(correo):
                print("Correo electrónico no válido. Intente nuevamente.")
                correo = input("Ingrese el correo del cliente: ")

            nota = Nota(cliente)

            fecha_inicio = input("Ingrese la fecha de inicio (DD-MM-YYYY): ")
            while True:
                try:
                    fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%d-%m-%Y')
                    if fecha_inicio <= datetime.datetime.now():
                        break
                    else:
                        print("La fecha de inicio no puede ser posterior a la fecha actual.")
                        fecha_inicio = input("Ingrese la fecha de inicio  (DD-MM-YYYY): ")
                except ValueError:
                    print("Formato de fecha incorrecto. Intente nuevamente.")
                    fecha_inicio = input("Ingrese la fecha de inicio (DD-MM-YYYY): ")

            fecha_fin = input("Ingrese la fecha de fin (DD-MM-YYYY): ")
            while True:
                try:
                    fecha_fin = datetime.datetime.strptime(fecha_fin, '%d-%m-%Y')
                    if fecha_fin >= fecha_inicio:
                        break
                    else:
                        print("La fecha de fin debe ser igual o posterior a la fecha de inicio.")
                        fecha_fin = input("Ingrese la fecha de fin (DD-MM-YYYY): ")
                except ValueError:
                    print("Formato de fecha incorrecto. Intente nuevamente.")
                    fecha_fin = input("Ingrese la fecha de fin (DD-MM-YYYY): ")

            nota.fecha_inicio = fecha_inicio.strftime('%d-%m-%Y')
            nota.fecha_fin = fecha_fin.strftime('%d-%m-%Y')
            nota.rfc = rfc
            nota.correo = correo

            servicios = []  

            while True:
                servicio_nombre = input("Ingrese el nombre del servicio: ")
                
                while True:
                    try:
                        servicio_precio = float(input("Ingrese el precio del servicio: "))
                        if servicio_precio <= 0:
                            print("El costo del servicio debe ser mayor que 0. Intente nuevamente.")
                        else:
                            break
                    except ValueError:
                        print("Formato de precio incorrecto. Intente nuevamente.")
                
                servicio = Servicio(servicio_nombre, servicio_precio)
                servicios.append(servicio)
                
                otra = ""
                while otra.upper() not in ('S', 'N'):
                    otra = input("\n¿Desea registrar otra servicio? (S/N): ")
                    if otra.upper() != 'S' and otra.upper() != 'N':
                        print("Respuesta no válida. Por favor, ingrese 'S' para sí o 'N' para no.")

                if otra.upper() != 'S':
                    break  

            nota.servicios = servicios  
            notas.append(nota)

            print("\nNota registrada exitosamente:")
            print(f"Folio: {nota.folio}")
            print(f"Cliente: {nota.cliente}")
            print(f"RFC: {nota.rfc}")
            print(f"Correo: {nota.correo}")
            print(f"Fecha de inicio: {nota.fecha_inicio}")
            print(f"Fecha de fin: {nota.fecha_fin}")
            print("Servicios:")
            for servicio in nota.servicios:
                print(f"- {servicio.nombre}: ${servicio.costo} MXN")
            print(f"Total: ${nota.calcular_total()} MXN")

            otra = ""
            while otra.upper() not in ('S', 'N'):
                otra = input("\n¿Desea registrar otra nota? (S/N): ")
                if otra.upper() != 'S' and otra.upper() != 'N':
                    print("Respuesta no válida. Por favor, ingrese 'S' para sí o 'N' para no.")

            if otra.upper() != 'S':
                break  
        except ValueError as e:
            print(f"Error: {e}")




def consultar_por_periodo(notas):
    fecha_inicial = input("Ingrese la fecha inicial (DD-MM-YYYY) (deje en blanco para 01-01-2000): ")
    fecha_final = input("Ingrese la fecha final (DD-MM-YYYY) (deje en blanco para fecha actual): ")

    if fecha_inicial == "":
        fecha_inicial = '01-01-2000'
    if fecha_final == "":
        fecha_final = datetime.datetime.now().strftime('%d-%m-%Y')
    
    try:
        fecha_inicial = datetime.datetime.strptime(fecha_inicial, '%d-%m-%Y')
        fecha_final = datetime.datetime.strptime(fecha_final, '%d-%m-%Y')
          
        if fecha_final >= fecha_inicial:
            notas_periodo = [nota for nota in notas if fecha_inicial <= datetime.datetime.strptime(nota.fecha_inicio, '%d-%m-%Y') <= fecha_final and not nota.cancelada]

            if len(notas_periodo) > 0:
                print("\nNotas en el período seleccionado:")
                for nota in notas_periodo:
                    print(f"Folio: {nota.folio}, Cliente: {nota.cliente}, Fecha de Inicio: {nota.fecha_inicio}, Monto Total: ${nota.calcular_total()} MXN")
            else:
                print("\nNo hay notas emitidas para el período seleccionado.")
        else:
            print("La fecha final debe ser igual o posterior a la fecha inicial.")
    except ValueError:
        print("Formato de fecha incorrecto.")



def consultar_por_folio(notas):
    folio = input("Ingrese el folio de la nota a consultar: ")
    
    try:
        folio = int(folio)
        nota = next((nota for nota in notas if nota.folio == folio), None)
        
        if nota and not nota.cancelada:
            print("\nDetalles de la nota:")
            print(f"Folio: {nota.folio}")
            print(f"Cliente: {nota.cliente}")
            print(f"RFC: {nota.rfc}")
            print(f"Correo: {nota.correo}")
            print(f"Fecha de inicio: {nota.fecha_inicio}")
            print(f"Fecha de fin: {nota.fecha_fin}")
            print("Servicios:")
            for servicio in nota.servicios:
                print(f"- {servicio.nombre}: ${servicio.costo} MXN")
            print(f"Total: ${nota.calcular_total()} MXN")
        elif nota and nota.cancelada:
            print("La nota está cancelada y no se puede consultar.")
        else:
            print("El folio indicado no existe.")
    except ValueError:
        print("Folio no válido.")

def consultar_por_cliente_y_exportar(notas):
    rfc_clientes = list(set(nota.rfc for nota in notas))
    rfc_clientes.sort()

    if not rfc_clientes:
        print("No hay RFCs de clientes con notas no canceladas")
        return

    print("\nLista de RFCs de clientes:")
    for i, rfc in enumerate(rfc_clientes, start=1):
        print(f"{i}. {rfc}")

    opcion_rfc = input("Seleccione el número correspondiente al RFC del cliente a consultar: ")

    try:
        opcion_rfc = int(opcion_rfc)
        if 1 <= opcion_rfc <= len(rfc_clientes):
            rfc_seleccionado = rfc_clientes[opcion_rfc - 1]
            notas_cliente = [nota for nota in notas if nota.rfc == rfc_seleccionado and not nota.cancelada]

            if not notas_cliente:
                print(f"No hay notas no canceladas disponibles para el cliente con RFC {rfc_seleccionado}")
            else:
                print(f"\nNotas del cliente con RFC {rfc_seleccionado}:")
                for nota in notas_cliente:
                    print(f"Folio: {nota.folio}, Fecha de Inicio: {nota.fecha_inicio}, Monto Total: ${nota.calcular_total()} MXN")
 
                monto_promedio = sum(nota.calcular_total() for nota in notas_cliente) / len(notas_cliente)
                print(f"Monto Promedio de Notas del Cliente: ${monto_promedio:.2f} MXN")


                exportar_excel = input("¿Desea exportar la información a un archivo de Excel? (S/N): ").strip().upper()
                if exportar_excel == "S":
                 
                    nombre_archivo = f"{rfc_seleccionado}_{fecha_actual()}.xlsx"
                    workbook = openpyxl.Workbook()
                    worksheet = workbook.active

                 
                    worksheet.append(["Folio", "Fecha de Inicio", "Monto Total (MXN)"])
                    for nota in notas_cliente:
                        worksheet.append([nota.folio, nota.fecha_inicio, nota.calcular_total()])

                  
                    for row in worksheet.iter_rows(min_row=2, max_row=len(notas_cliente) + 1):
                        for cell in row:
                            cell.alignment = Alignment(horizontal='center')

                  
                    workbook.save(nombre_archivo)
                    print(f"Archivo de Excel '{nombre_archivo}' creado con éxito.")
        else:
            print("Opción no válida.")
    except ValueError:
        print("Opción no válida.")




def cancelar_nota(notas):
    folio = input("Ingrese el folio de la nota que desea cancelar: ")
    
    try:
        folio = int(folio)
        nota = next((nota for nota in notas if nota.folio == folio), None)
        
        if nota and not nota.cancelada:
            print("\nDetalles de la nota a cancelar:")
            print(f"Folio: {nota.folio}")
            print(f"Cliente: {nota.cliente}")
            print(f"Fecha de inicio: {nota.fecha_inicio}")
            print("Servicios:")
            for servicio in nota.servicios:
                print(f"- {servicio.nombre}: ${servicio.costo} MXN")
            print(f"Total: ${nota.calcular_total()} MXN")
            
            confirmar = input("¿Está seguro de que desea cancelar esta nota? (S/N): ").strip().upper()
            if confirmar == "S":
                nota.cancelada = True
                print("La nota ha sido cancelada.")
            else:
                print("La nota no ha sido cancelada.")
        elif nota and nota.cancelada:
            print("La nota ya está cancelada.")
        else:
            print("El folio indicado no existe.")
    except ValueError:
        print("Folio no válido.")


def recuperar_nota_cancelada(notas):
    notas_canceladas = [nota for nota in notas if nota.cancelada]
    
    if not notas_canceladas:
        print("\nNo hay notas canceladas para recuperar.")
        return
    
    print("\nNotas canceladas:")
    for i, nota in enumerate(notas_canceladas, start=1):
        print(f"{i}. Folio: {nota.folio}, Cliente: {nota.cliente}, Fecha de Inicio: {nota.fecha_inicio}")
    
    opcion_recuperar = input("Seleccione el número correspondiente al folio de la nota que desea recuperar (0 para cancelar): ")
    
    try:
        opcion_recuperar = int(opcion_recuperar)
        if 0 <= opcion_recuperar <= len(notas_canceladas):
            if opcion_recuperar == 0:
                print("No se ha recuperado ninguna nota.")
            else:
                nota = notas_canceladas[opcion_recuperar - 1]
                nota.cancelada = False
                print(f"\nLa nota con folio {nota.folio} ha sido recuperada.")
        else:
            print("Opción no válida.")
    except ValueError:
        print("Opción no válida.")



def cargar_estado():
    notas = []
    if os.path.exists('estado_aplicacion.csv'):
        with open('estado_aplicacion.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                folio, fecha_inicio, fecha_fin, cliente, rfc, correo, cancelada, servicios_info = row
                nota = Nota(cliente)
                nota.folio = int(folio)
                nota.fecha_inicio = fecha_inicio
                nota.fecha_fin = fecha_fin
                nota.rfc = rfc
                nota.correo = correo
                nota.cancelada = cancelada.lower() == 'true'
                
                servicios_info = servicios_info.split(';')
                for servicio_info in servicios_info:
                    servicio_nombre, servicio_precio = servicio_info.split(':')
                    servicio = Servicio(servicio_nombre, float(servicio_precio))
                    nota.agregar_servicio(servicio)

                notas.append(nota)
    else:
        print("\nNo se encontró un estado previo. Partiendo de un estado inicial vacío.")
    return notas

def guardar_estado(notas):
    with open('estado_aplicacion.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Folio", "Fecha de Inicio", "Fecha de Fin", "Cliente", "RFC", "Correo", "Cancelada", "Servicios"])
        for nota in notas:
            servicios_info = ";".join([f"{servicio.nombre}:{servicio.costo}" for servicio in nota.servicios])

            writer.writerow([nota.folio, nota.fecha_inicio, nota.fecha_fin, nota.cliente, nota.rfc, nota.correo, str(nota.cancelada), servicios_info])

    print("Estado de la aplicación guardado correctamente.")

def main():
    notas = cargar_estado()

    while True:
        print

        print("\nMenú Principal")
        print("1. Registrar una nota")
        print("2. Consultas y Reportes")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota cancelada")
        print("5. Salir\n")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_nota(notas)

        elif opcion == '2':
            while True:
                print("\nSubmenú - Consultas y Reportes")
                print("1. Consulta por período")
                print("2. Consulta por folio")
                print("3. Consulta por cliente y exportar a Excel")
                print("4. Volver al menú principal\n")

                opcion_consulta = input("Seleccione una opción: ")

                if opcion_consulta == '1':
                    consultar_por_periodo(notas)

                elif opcion_consulta == '2':
                  
                    consultar_por_folio(notas)

                elif opcion_consulta == '3':
                    consultar_por_cliente_y_exportar(notas)

                elif opcion_consulta == '4':
                    break

                else:
                    print("\nOpción no válida. Intente de nuevo.")

        elif opcion == '3':
            cancelar_nota(notas)

        elif opcion == '4':
            recuperar_nota_cancelada(notas)

        elif opcion == '5':
            confirmacion = input("¿Desea salir? (S/N): ").upper()
            if confirmacion == 'S':
                guardar_estado(notas)
                print("¡Hasta luego!")
                break
            elif confirmacion == 'N':
                continue
            else:
                print("\nOpción no válida. Intente de nuevo.")
        else:
            print("\nOpción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
