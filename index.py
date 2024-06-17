import math
from flask import Flask, render_template, request
from BCU.BCU import buscar_solucion_UCS
from BCU.BSF import Nodo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/busqueda_costo_uniforme', methods=['POST'])
def busqueda_costo_uniforme_route():
    start_city = request.form['start_city']
    end_city = request.form['end_city']
    
    coord = {
        'Aguascalientes': (21.88234, -102.28259),
        'Baja California': (32.6519, -115.46833),
        'Baja California Sur': (24.14437, -110.3005),
        'Campeche': (19.84577, -90.52554),
        'Chiapas': (16.75, -93.11667),
        'Chihuahua': (28.63528, -106.08889),
        'Ciudad de México': (19.432608, -99.133209),
        'Coahuila': (25.43333, -100.96667),
        'Colima': (19.24333, -103.725),
        'Durango': (24.02222, -104.65333),
        'Guanajuato': (21.01778, -101.25667),
        'Guerrero': (17.55139, -99.50056),
        'Hidalgo': (20.11697, -98.73329),
        'Jalisco': (20.66682, -103.39182),
        'México': (19.35867, -99.68156),
        'Michoacán': (19.70556, -101.195),
        'Morelos': (18.91667, -99.25),
        'Nayarit': (21.50833, -104.895),
        'Nuevo León': (25.66667, -100.31667),
        'Oaxaca': (17.05944, -96.72556),
        'Puebla': (19.04344, -98.19807),
        'Querétaro': (20.58806, -100.38806),
        'Quintana Roo': (18.50361, -88.30528),
        'San Luis Potosí': (22.15, -100.98333),
        'Sinaloa': (24.80906, -107.394),
        'Sonora': (29.07297, -110.95592),
        'Tabasco': (17.98917, -92.9475),
        'Tamaulipas': (24.26694, -98.83628),
        'Tlaxcala': (19.31392, -98.24128),
        'Veracruz': (19.19, -96.15306),
        'Yucatán': (20.96667, -89.61667),
        'Zacatecas': (22.76842, -102.58141)
    }
    
    conexiones = {
        'Aguascalientes': {'Zacatecas': 120, 'San Luis Potosí': 130, 'Jalisco': 200, 'Guanajuato': 120},
        'Baja California': {'Baja California Sur': 1600, 'Sonora': 820},
        'Baja California Sur': {'Baja California': 1600, 'Sinaloa': 220},
        'Campeche': {'Yucatán': 190, 'Tabasco': 170},
        'Chiapas': {'Tabasco': 210, 'Oaxaca': 300, 'Veracruz': 370},
        'Chihuahua': {'Sonora': 690, 'Coahuila': 570, 'Durango': 600},
        'Ciudad de México': {'México': 50, 'Puebla': 120, 'Morelos': 70, 'Querétaro': 210, 'Hidalgo': 90},
        'Coahuila': {'Nuevo León': 280, 'Durango': 410, 'Chihuahua': 570},
        'Colima': {'Jalisco': 150, 'Michoacán': 220},
        'Durango': {'Chihuahua': 600, 'Sinaloa': 200, 'Zacatecas': 320, 'Coahuila': 410},
        'Guanajuato': {'Aguascalientes': 120, 'Jalisco': 190, 'Querétaro': 140, 'Michoacán': 170},
        'Guerrero': {'Morelos': 170, 'Michoacán': 320, 'Oaxaca': 230},
        'Hidalgo': {'Ciudad de México': 90, 'Querétaro': 180, 'San Luis Potosí': 260},
        'Jalisco': {'Aguascalientes': 200, 'Guanajuato': 190, 'Colima': 150, 'Michoacán': 290, 'Nayarit': 220},
        'México': {'Ciudad de México': 50, 'Querétaro': 180, 'Puebla': 140, 'Morelos': 90},
        'Michoacán': {'Jalisco': 290, 'Guanajuato': 170, 'Guerrero': 320, 'Colima': 220},
        'Morelos': {'Ciudad de México': 70, 'México': 90, 'Guerrero': 170, 'Puebla': 160},
        'Nayarit': {'Jalisco': 220, 'Sinaloa': 420},
        'Nuevo León': {'Coahuila': 280, 'San Luis Potosí': 300, 'Tamaulipas': 220},
        'Oaxaca': {'Chiapas': 300, 'Guerrero': 230, 'Puebla': 340, 'Veracruz': 260},
        'Puebla': {'Ciudad de México': 120, 'México': 140, 'Veracruz': 250, 'Oaxaca': 340, 'Tlaxcala': 40},
        'Querétaro': {'Ciudad de México': 210, 'Hidalgo': 180, 'México': 180, 'Guanajuato': 140, 'San Luis Potosí': 190},
        'Quintana Roo': {'Yucatán': 320, 'Campeche': 510},
        'San Luis Potosí': {'Aguascalientes': 130, 'Querétaro': 190, 'Hidalgo': 260, 'Nuevo León': 300, 'Zacatecas': 190},
        'Sinaloa': {'Baja California Sur': 220, 'Durango': 200, 'Sonora': 520, 'Nayarit': 420},
        'Sonora': {'Chihuahua': 690, 'Sinaloa': 520, 'Baja California': 820},
        'Tabasco': {'Campeche': 170, 'Chiapas': 210, 'Veracruz': 320},
        'Tamaulipas': {'Nuevo León': 220, 'Veracruz': 480},
        'Tlaxcala': {'Puebla': 40, 'Veracruz': 200},
        'Veracruz': {'Puebla': 250, 'Oaxaca': 260, 'Tabasco': 320, 'Tamaulipas': 480, 'Tlaxcala': 200},
        'Yucatán': {'Campeche': 190, 'Quintana Roo': 320},
        'Zacatecas': {'Aguascalientes': 120, 'San Luis Potosí': 190, 'Durango': 320}
    }
 
    if start_city not in coord or end_city not in coord:
        return "Ciudad de inicio o destino no válidas", 400

    nodo_solucion = buscar_solucion_UCS(conexiones, start_city, end_city)
    
    if nodo_solucion is None:
        return f"No se encontró una ruta de {start_city} a {end_city}", 400

    resultado = []
    nodo = nodo_solucion

    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()

    resultado.append(start_city)
    resultado.reverse()

    distancia_total = nodo_solucion.get_costo()

    coordenadas_ruta = [coord[ciudad] for ciudad in resultado]
    
    return render_template('result.html', algoritmo='Ruta Optima', ruta=resultado, distancia_total=distancia_total, coordenadas_ruta=coordenadas_ruta, start_city=start_city, end_city=end_city)

if __name__ == '__main__':
    app.run(debug=True)
