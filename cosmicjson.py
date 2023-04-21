import json
import os

group = "BuiltinCommonInstructions::Group"
standard = "BuiltinCommonInstructions::Standard"
moreSubInstructions = ["BuiltinCommonInstructions::And", "BuiltinCommonInstructions::Or", "BuiltinCommonInstructions::Not"]
counter = 0

def ready_to_exit():
    input("Presiona cualquier tecla para salir...")
    exit()

def change_key_values(condition):
    global counter
    if (condition["type"]["value"] == "KeyReleased" and condition["parameters"][1] == key_name):
        condition["type"]["value"] = "KeyFromTextReleased"
        condition["parameters"][1] = "GlobalVariableString(" + str(variable_name) + ")"
        counter += 1
    if (condition["type"]["value"] == "KeyPressed" and condition["parameters"][1] == key_name):
        condition["type"]["value"] = "KeyFromTextPressed"
        condition["parameters"][1] = "GlobalVariableString(" + str(variable_name) + ")"
        counter += 1

def change_mouse_values(condition):
    global counter
    if (condition["type"]["value"] == "MouseButtonReleased" and condition["parameters"][1] == mouse_dir):
        condition["type"]["value"] = "KeyReleased"
        condition["parameters"][1] = new_key_name
        counter += 1
    if (condition["type"]["value"] == "MouseButtonPressed" and condition["parameters"][1] == mouse_dir):
        condition["type"]["value"] = "KeyPressed"
        condition["parameters"][1] = new_key_name
        counter += 1

def iterate_through_conditions(condition):
    more_conditions = condition.get("subInstructions")
    if (more_conditions is not None):
        for sub_condition in more_conditions:
            iterate_through_conditions(sub_condition)
    if (mode == 1):
        change_key_values(condition)
    else:
        change_mouse_values(condition)

def iterate_trough_events(event):
    more_events = event.get("events")
    if (more_events is not None):
        for sub_event in more_events:
            iterate_trough_events(sub_event)
    if (event["type"] == standard):
        for condition in event["conditions"]:
            iterate_through_conditions(condition)

def init_iteration():
    try:
        for layout in data["layouts"]:
            for event in layout["events"]:
                iterate_trough_events(event)
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")
        ready_to_exit()



print("   ____                    _              _                 ")
print("  / ___|___  ___ _ __ ___ (_) ___        (_)___  ___  _ __  ")
print(" | |   / _ \/ __| '_ ` _ \| |/ __|       | / __|/ _ \| '_ \ ")
print(" | |__| (_) \__ \ | | | | | | (__   _    | \__ \ (_) | | | |")
print("  \____\___/|___/_| |_| |_|_|\___| (_)  _/ |___/\___/|_| |_|")
print("                                       |__/                 ")
mode = input("\n\nIntroduce el modo: ")
try:
    mode = int(mode)
    if not mode in range(1, 3):
        print("Modo no disponible. Consulta los modos disponiles.")
        ready_to_exit()

except ValueError:
    print("Ese no es un número válido")
    ready_to_exit()

file_name = input("Introduce el nombre del archivo json (ex: juego.json): ")

if (not os.path.exists(file_name)):
    print("El nombre del archivo .json que has introducido no existe en el directorio actual")
    ready_to_exit()

try:
    with open(file_name, "r") as f:
        data = json.load(f)

    if (mode == 1):
        key_name = input("Introduce el nombre de la tecla que deseas cambiar: ")
        variable_name = input("Introduce el nombre de la variable que irá dentro de GlobalVariableString: ")
    else:
        new_key_name = input("Introduce el nombre de la tecla por la cual será substituido el ratón: ")
        mouse_dir = input("Introduce el click del raton que quieres cambiar (Left o Right): ")
        if (not mouse_dir in ["Left", "Right"]):
            print("Has introducido un valor incorrecto.")
            ready_to_exit()

    init_iteration()

    print(f"Un total de {counter} condiciones han sido modificadas con éxito")
    name_only = os.path.splitext(os.path.basename(file_name))[0]
    with open(name_only + "_cosmic.json", "w") as f:
        json.dump(data, f, indent=4)

except FileNotFoundError:
    print(f"No se encontró el archivo {file_name}.json")

except Exception as e:
    print(f"Error inesperado: {e}")

ready_to_exit()
