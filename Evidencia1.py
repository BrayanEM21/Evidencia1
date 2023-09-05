import datetime




class Servicio:
    def __init__(self, nombre, costo):
        self.nombre = nombre
        self.costo = costo



servicios_disponibles = [
    Servicio("Cambio de aceite y filtro", 800),
    Servicio("Reemplazo de frenos delanteros (pastillas y discos)", 1500),
    Servicio("Alineación y balanceo de ruedas", 600),
    Servicio("Cambio de batería", 1200),
    Servicio("Reparación de sistema de aire acondicionado", 1800),
    Servicio("Cambio de bujías y cables", 600),
    Servicio("Reemplazo de alternador", 2500),
    Servicio("Reparación de sistema eléctrico", 1000),
    Servicio("Cambio de kit de distribución", 2000),
    Servicio("Reparación de sistema de dirección asistida", 1500),
    Servicio("Cambio de filtro de aire", 400),
    Servicio("Reparación de sistema de frenos traseros", 1300),
    Servicio("Cambio de líquido de transmisión", 1100),
    Servicio("Inspección general del vehículo", 500),
    Servicio("Recarga de refrigerante de aire acondicionado", 700),
    Servicio("Cambio de filtro de combustible", 450),
    Servicio("Reparación de sistema de escape", 800),
    Servicio("Cambio de líquido de frenos", 600),
    Servicio("Ajuste de motor y rendimiento", 950)
]


class Nota:
    folio_counter = 1
    
    def __init__(self, cliente):
        self.folio = Nota.folio_counter
        Nota.folio_counter += 1
        self.fecha = datetime.datetime.now()
        self.cliente = cliente
        self.cancelada = False
        self.servicios = []

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def calcular_total(self):
        total = sum(servicio.costo for servicio in self.servicios)
        return total
    


def mostrar_menu_principal():
    print("\nMenú principal:")
    print("1. Registrar una nota")
    print("2. Consultas y reportes")
    print("3. Cancelar una nota")
    print("4. Recuperar una nota")
    print("5. Salir")


def mostrar_submenu_consultas():
    print("\nSubmenú de Consultas y Reportes:")
    print("1. Consulta por período")
    print("2. Consulta por folio")
    print("Presione Enter para regresar al Menú Principal...")


def mostrar_servicios_disponibles():
    print("\nServicios disponibles:")
    for index, servicio in enumerate(servicios_disponibles, start=1):
        print(f"{index}. {servicio.nombre} - ${servicio.costo} MXN")




def registrar_nota(notas):
    cliente = input("Ingrese el nombre del cliente: ")
    nota = Nota(cliente)
            
    mostrar_servicios_disponibles()
    num_servicios = int(input("Ingrese la cantidad de servicios que desea agregar: "))
            
    for _ in range(num_servicios):
        mostrar_servicios_disponibles()
        indice_servicio = int(input(f"Ingrese el número de servicio {_ + 1}: "))
        servicio_elegido = servicios_disponibles[indice_servicio - 1]
        nota.agregar_servicio(servicio_elegido)
            
    notas.append(nota)
    
    print("\nNota registrada exitosamente:")
    print(f"Folio: {nota.folio}")
    print(f"Cliente: {nota.cliente}")
    print(f"Fecha: {nota.fecha.date()}")
    print("Servicios:")
    for servicio in nota.servicios:
        print(f"- {servicio.nombre}: ${servicio.costo} MXN")
    print(f"Total: ${nota.calcular_total()} MXN")
    
    input("\nPresione Enter para regresar al Menú Principal...")



def consulta_por_periodo(notas):
    fecha_inicio_str = input("Ingrese la fecha de inicio (dd/mm/aaaa): ")
    fecha_fin_str = input("Ingrese la fecha de fin (dd/mm/aaaa): ")

    try:
        fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
        fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%d/%m/%Y")
        fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)

        notas_en_periodo = [nota for nota in notas if fecha_inicio <= nota.fecha <= fecha_fin and not nota.cancelada]

        if notas_en_periodo:
            print("\nReporte de Notas en el período seleccionado:")
            print("{:<10} {:<20} {}".format("Folio", "Cliente", "Fecha"))
            print("="*45)
            for nota in notas_en_periodo:
                fecha_modificada = nota.fecha.strftime("%d/%m/%Y")
                print("{:<10} {:<20} {}".format(nota.folio, nota.cliente, fecha_modificada))
        else:
            print("\nNo hay notas emitidas para el período seleccionado.")
    except ValueError:
        print("Formato de fecha incorrecto. Ingrese las fechas en el formato dd/mm/aaaa.")

    input("\nPresione Enter para regresar al Menú Principal...")




def consulta_por_folio(notas):
    folio_buscar = int(input("Ingrese el folio de la nota a buscar: "))
    
    nota_encontrada = None
    for nota in notas:
        if nota.folio == folio_buscar:
            nota_encontrada = nota
            break
    
    if nota_encontrada and not nota_encontrada.cancelada:
        print("\nNota encontrada:")
        print(f"Folio: {nota_encontrada.folio}")
        print(f"Cliente: {nota_encontrada.cliente}")
        print(f"Fecha: {nota_encontrada.fecha}")
        print("Servicios:")
        for servicio in nota_encontrada.servicios:
            print(f"- {servicio.nombre}: ${servicio.costo} MXN")
        print(f"Total: ${nota_encontrada.calcular_total()} MXN")
    else:
        print("\nNota no encontrada o cancelada.")



def cancelar_nota(notas):
    folio_cancelar = input("Ingrese el folio de la nota a cancelar: ")

    try:
        folio_cancelar = int(folio_cancelar)
        nota_cancelar = next((nota for nota in notas if nota.folio == folio_cancelar), None)

        if nota_cancelar and not nota_cancelar.cancelada:
            print("\nDetalle de la nota a cancelar:")
            print(f"Folio: {nota_cancelar.folio}")
            print(f"Cliente: {nota_cancelar.cliente}")
            print(f"Fecha: {nota_cancelar.fecha}")
            print("Servicios:")
            for servicio in nota_cancelar.servicios:
                print(f"- {servicio.nombre}: ${servicio.costo} MXN")
            print(f"Total: ${nota_cancelar.calcular_total()} MXN")

            confirmacion = input("\n¿Desea cancelar esta nota? (S/N): ")
            if confirmacion.lower() == 's':
                nota_cancelar.cancelada = True
                print("Nota cancelada exitosamente.")
            else:
                print("Cancelación de nota cancelada.")
        elif nota_cancelar and nota_cancelar.cancelada:
            print("La nota ya está cancelada en el sistema.")
        else:
            print("El folio ingresado no corresponde a una nota existente en el sistema.")

    except ValueError:
        print("Por favor, ingrese un número de folio válido.")

    input("\nPresione Enter para regresar al Menú Principal...")

    


def recuperar_nota_cancelada(notas):
    notas_canceladas = [nota for nota in notas if nota.cancelada]

    if notas_canceladas:
        print("\nNotas actualmente canceladas:")
        print("{:<10} {:<20}".format("Folio", "Cliente"))
        print("="*30)
        for nota in notas_canceladas:
            print("{:<10} {:<20}".format(nota.folio, nota.cliente))

        folio_recuperar = input("\nIngrese el folio de la nota que desea recuperar (o 'n' para cancelar): ")

        if folio_recuperar.lower() == 'n':
            print("No se ha realizado la recuperación de ninguna nota.")
        else:
            try:
                folio_recuperar = int(folio_recuperar)
                nota_recuperar = next((nota for nota in notas_canceladas if nota.folio == folio_recuperar), None)
                if nota_recuperar:
                    print("\nDetalle de la nota:")
                    print(f"Folio: {nota_recuperar.folio}")
                    print(f"Cliente: {nota_recuperar.cliente}")
                    print(f"Fecha: {nota_recuperar.fecha}")
                    print("Servicios:")
                    for servicio in nota_recuperar.servicios:
                        print(f"- {servicio.nombre}: ${servicio.costo} MXN")
                    print(f"Total: ${nota_recuperar.calcular_total()} MXN")

                    confirmacion = input("\n¿Desea recuperar esta nota? (S/N): ")
                    if confirmacion.lower() == 's':
                        nota_recuperar.cancelada = False
                        print("Nota recuperada exitosamente.")
                    else:
                        print("Recuperación cancelada.")
                else:
                    print("El folio ingresado no corresponde a una nota cancelada.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    else:
        print("\nNo hay notas canceladas para recuperar.")

    input("\nPresione Enter para regresar al Menú Principal...")






def main():
    notas = []
    
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        
        try:
            opcion = int(opcion)
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
        
        if opcion == 1:
            registrar_nota(notas)
        elif opcion == 2:
            mostrar_submenu_consultas()
            subopcion = input("Seleccione una opción: ")
            
            try:
                subopcion = int(subopcion)
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue
            
            if subopcion == 1:
                consulta_por_periodo(notas)
            elif subopcion == 2:
                consulta_por_folio(notas)
        
        elif opcion == 3:
            cancelar_nota(notas)
        
        elif opcion == 4:
            recuperar_nota_cancelada(notas)
        
        elif opcion == 5:
            confirmacion = input("¿Desea salir? (S/N): ")
            if confirmacion.lower() == 's':
                break
        
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
