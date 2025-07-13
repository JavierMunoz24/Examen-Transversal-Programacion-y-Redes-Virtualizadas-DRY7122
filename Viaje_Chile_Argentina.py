import requests

def geocodificar(ciudad, api_key):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        resultados = response.json()
        if resultados["hits"]:
            punto = resultados["hits"][0]
            return f"{punto['point']['lat']},{punto['point']['lng']}"
        else:
            print(f"No se encontró la ciudad: {ciudad}")
            return None
    else:
        print("Error en la geocodificación:", response.text)
        return None

def obtener_datos(origen_coord, destino_coord, transporte, api_key):
    url = "https://graphhopper.com/api/1/route"

    params = {
        "point": [origen_coord, destino_coord],
        "vehicle": transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener datos de ruta:", response.text)
        return None

def mostrar_resultados(datos):
    path = datos["paths"][0]
    distancia_km = path["distance"] / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_horas = path["time"] / (1000 * 60 * 60)

    print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
    print(f"Duración estimada: {duracion_horas:.2f} horas")
    print("Narrativa del viaje:")
    for paso in path["instructions"]:
        print(f"- {paso['text']}")

def main():
    api_key = "ebb33397-d8cd-4a84-8264-167e0aa0dcb3"

    print("==== Calculadora de Rutas Chile - Argentina ====")

    while True:
        ciudad_origen = input("\nCiudad de origen (o 's' para salir): ").strip()
        if ciudad_origen.lower() == 's':
            break

        ciudad_destino = input("Ciudad de destino (o 's' para salir): ").strip()
        if ciudad_destino.lower() == 's':
            break

        print("\nSelecciona el medio de transporte:")
        print("1. Automóvil")
        print("2. Bicicleta")
        print("3. A pie")
        opcion = input("Opción (1/2/3): ").strip()
        transporte = {"1": "car", "2": "bike", "3": "foot"}.get(opcion, "car")

        origen_coord = geocodificar(ciudad_origen, api_key)
        destino_coord = geocodificar(ciudad_destino, api_key)

        if origen_coord and destino_coord:
            datos = obtener_datos(origen_coord, destino_coord, transporte, api_key)
            if datos:
                mostrar_resultados(datos)

if __name__ == "__main__":
    main()
