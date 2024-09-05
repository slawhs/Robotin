from jsonpath_ng.ext import parse
import json
import os

def place_query(place_name: str) -> list:
    """Retorna una lista con la ubicación (coordenadas) de un lugar de la universidad a partir su nombre. Si la lista no es vacía, entonces es una ubicación válida."""

    with open(os.path.join('src', 'LLM', 'data', 'places.json')) as f:
        json_data = json.load(f)

    place_code = ""

    if  place_name.lower().startswith("sala"):
        place_code = place_name.strip("sala ")
        place_code = place_code.strip("Sala ")
        place_code = place_code.strip("SALA ")

    elif place_name.lower().startswith("auditorio"):
        place_code = place_name.strip("auditorio")
        place_code = place_code.strip("Auditorio ")
        place_code = place_code.strip("AUDITORIO ")

    print(f"place_code: {place_code}")

    try:
        # Definir la expresión JSONPath
        jsonpath_expr = parse(f"$.places[?(@.name =~ '{place_code.upper()}')].coordinates")
        # Ejecutar la consulta JSONPath
        result = jsonpath_expr.find(json_data)
        # Mostrar los resultados
        coordinates = [match.value for match in result]

        print(f"coordinates: {coordinates}")

        if coordinates == []:
            return("Error, no se encontró un lugar.")
        
        return(coordinates[0][::-1])


    except ValueError as e:
        return("Error encontrando el lugar. + Info:", e)

            

        