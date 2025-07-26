import os
import re
import math
import datetime
import random
from Helpers.utils import logWriter, txtWriter
 
def readPointsFromGaussJordan():
    """
    Lee los puntos desde el archivo GaussJordan.txt
    
    Returns:
        list: Lista de tuplas [(x, y, z), ...] o None si hay error
    """
    try:
        scriptDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gaussJordanFile = os.path.join(scriptDir, "Storage", "GaussJordan.txt")
        
        if not os.path.exists(gaussJordanFile):
            logWriter("Error: Archivo GaussJordan.txt no encontrado", True)
            return None
            
        points = []
        with open(gaussJordanFile, 'r', encoding='utf-8') as file:

            firstLine = file.readline()
            

            for i, line in enumerate(file):
                if i >= 5:
                    break
                
                line = line.strip()
                if not line:
                    continue
                

                match = re.match(r'x:([-+]?\d*\.?\d+)#y:([-+]?\d*\.?\d+)#z:([-+]?\d*\.?\d+)', line)
                if match:
                    x, y, z = float(match.group(1)), float(match.group(2)), float(match.group(3))
                    points.append((x, y, z))
                else:
                    logWriter(f"Error: Formato de coordenadas inválido en línea: {line}", True)
        
        return points
        
    except Exception as e:
        logWriter(f"Error leyendo puntos desde GaussJordan.txt: {str(e)}", True)
        return None

def calculateEuclideanDistance(point1, point2):
    """
    Calcula la distancia euclidiana entre dos puntos 3D
    
    Args:
        point1: tupla (x, y, z)
        point2: tupla (x, y, z)
        
    Returns:
        float: distancia euclidiana
    """
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def generateDistanceReport():
    """
    Genera un reporte de distancias entre todos los pares de puntos
    """
    try:
 
        points = readPointsFromGaussJordan()
        
        if points is None:
            logWriter("Error: No se pudieron leer los puntos", True)
            return False
            
        if len(points) < 2:
            logWriter("Se necesitan al menos 2 puntos para calcular distancias", True)

            generateDistanceFile([], "No se pueden calcular distancias: se necesitan al menos 2 puntos")
            return True
        

        distances = []
        numPoints = len(points)
        
        for i in range(numPoints):
            for j in range(i + 1, numPoints):
                point1 = points[i]
                point2 = points[j]
                distance = calculateEuclideanDistance(point1, point2)
                
                distances.append({
                    'point1_idx': i + 1,
                    'point2_idx': j + 1,
                    'point1_coords': point1,
                    'point2_coords': point2,
                    'distance': distance
                })
        

        generateDistanceFile(distances)
        return True
        
    except Exception as e:
        logWriter(f"Error generando reporte de distancias: {str(e)}", True)
        return False

def generateDistanceFile(distances, errorMessage=None):
    """
    Genera el archivo de distancias con nombre único
    """
    try:

        currentDateTime = datetime.datetime.now()
        formattedDateTime = currentDateTime.strftime("%Y-%m-%d_%H-%M-%S")
        randNum = random.randint(1, 99)
        outputFileName = f"Resultado_Notacion_Complejo_{formattedDateTime}_serial{randNum}"
        

        if errorMessage:
            content = errorMessage
        else:
            contentLines = []
            for distInfo in distances:
                point1Coords = distInfo['point1_coords']
                point2Coords = distInfo['point2_coords']
                distance = distInfo['distance']
                

                def formatCoord(value):
                    formatted = f"{value:.6f}"
                    return formatted.replace('-', '−')
                

                p1X, p1Y, p1Z = formatCoord(point1Coords[0]), formatCoord(point1Coords[1]), formatCoord(point1Coords[2])
                p2X, p2Y, p2Z = formatCoord(point2Coords[0]), formatCoord(point2Coords[1]), formatCoord(point2Coords[2])
                distFormatted = f"{distance:.6f}"
                

                line = f"P{distInfo['point1_idx']}=({p1X},{p1Y},{p1Z}) y P{distInfo['point2_idx']}=({p2X},{p2Y},{p2Z}), ambos elementos del conjunto R³. {{(P{distInfo['point1_idx']},P{distInfo['point2_idx']},{distFormatted})∣P{distInfo['point1_idx']}=({p1X},{p1Y},{p1Z})∧P{distInfo['point2_idx']}=({p2X},{p2Y},{p2Z})}}"
                contentLines.append(line)
            
            content = "\n".join(contentLines)
        
        txtWriter(outputFileName, content, False)
        
    except Exception as e:
        logWriter(f"Error generando archivo de distancias: {str(e)}", True) 