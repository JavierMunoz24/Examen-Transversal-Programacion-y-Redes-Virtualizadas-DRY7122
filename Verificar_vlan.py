try:
    vlan = int(input("Ingrese el número de VLAN: "))

    if 1 <= vlan <= 1005:
        print(f"VLAN {vlan} pertenece al rango NORMAL (1–1005).")
    elif 1006 <= vlan <= 4094:
        print(f"VLAN {vlan} pertenece al rango EXTENDIDO (1006–4094).")
    elif vlan == 0 or vlan > 4094:
        print("VLAN fuera de rango permitido (1–4094).")
    else:
        print("VLAN reservada o inválida.")
except ValueError:
    print("Entrada inválida. Debe ingresar un número entero.")
