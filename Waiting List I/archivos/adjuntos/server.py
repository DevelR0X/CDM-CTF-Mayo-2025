from datetime import datetime
from util import MEMORY, RSA

# Procesa una entrada de cita en formato texto
def process_appointment(input_str):
    parts = input_str.strip().split(';')
    if len(parts) != 4:
        print("Formato inválido. Usa: nombre;apellido;dd-mm-aaaa;hh:mm")
        return None

    try:
        return datetime.strptime(f'{parts[2]} {parts[3]}', '%d-%m-%Y %H:%M')
    except ValueError:
        print("Fecha u hora inválida. Usa formatos dd-mm-aaaa y hh:mm.")
        return None

# Menú del sistema de gestión de citas del Hospital Eloísa Díaz
def main():
    try:
        FLAG = open("flag.txt", "r").read().strip()
    except:
        FLAG = "CDM{f4k3_fl4G_f0r_73571nG...}"

    memory = MEMORY()
    rsa = RSA(memory)

    appointments = open("citas.txt", "r").readlines()
    first_date = process_appointment(appointments[1])
    last_date = process_appointment(appointments[-1])

    print("=== Hospital Eloísa Díaz - Sistema de Administración de Gestión de Citas ===")
    print(f"Llave pública: {rsa.public_key}")
    print("[1] Solicitar nueva cita")
    print("[2] Confirmar cita existente")
    print("[3] Eliminar caché")
    print("[4] Regenerar llaves RSA")
    print("[5] Salir")

    while True:
        option = input("\n> ")

        if option == "1":
            appointment = input(
                "\nIngrese su cita en el siguiente formato:\n"
                "nombre;apellido;dd-mm-aaaa;hh:mm\n> "
            )
            date = process_appointment(appointment)

            if not date:
                continue

            if date > last_date:
                signature = rsa.sign(appointment.encode())
                print(f"\n✔️  Cita registrada con éxito.\nFirma digital: {signature}")
            else:
                print(f"\n❌ No quedan horas disponibles antes de {last_date.strftime('%d-%m-%Y')};{last_date.strftime('%H:%M')}.")

        elif option == "2":
            appointment = input("\nIngrese su cita: ")
            date = process_appointment(appointment)

            if not date:
                continue

            try:
                signature = int(input("Ingrese la firma de su cita: "))
            except ValueError:
                print("Firma inválida.")
                continue

            if rsa.verify(appointment.encode(), signature):
                print("✅ Cita confirmada.")
                if date > last_date:
                    last_date = date
                elif date < first_date:
                    print(f"\n🔓 Estimado paciente, será atendido inmediatamente. Presente el código {FLAG} al médico especialista.")
            else:
                print("❌ Firma inválida.")

        elif option == "3":
            appointment = input("\nIngrese su cita: ")
            try:
                slot = int(input("Slot a limpiar: "))
            except ValueError:
                print("Slot inválido.")
                continue
            rsa.reset_cache(appointment.encode(), slot)

        elif option == "4":
            rsa.keygen()
            print(f"🔑 Llaves RSA regeneradas: {rsa.public_key}.")

        elif option == "5":
            print("Saliendo del sistema.")
            break

        else:
            print("Opción inválida.")

if __name__ == '__main__':
    main()