from django.shortcuts import render
import plotly.graph_objs as go
from plotly.offline import plot

from django.shortcuts import render
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np

def grafica_3d(request):
    # Simulación: recibe los datos del backend (array de strings)
    coordenadas = np.array(["1.2/3.4/5.6", "-2.0/0.0/4.1", "invalid"])  # ← usa tu array real aquí

    # Filtrar y convertir los puntos válidos
    puntos_validos = []
    for c in coordenadas:
        if c != "invalid":
            try:
                x_str, y_str, z_str = c.split('/')
                x, y, z = float(x_str), float(y_str), float(z_str)
                puntos_validos.append((x, y, z))
            except ValueError:
                continue  # por si hay un error de formato inesperado

    if not puntos_validos:
        plot_div = "<p>No hay puntos válidos para graficar.</p>"
    else:
        x = [p[0] for p in puntos_validos]
        y = [p[1] for p in puntos_validos]
        z = [p[2] for p in puntos_validos]

        trace = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers+lines',
            marker=dict(size=5, color='red'),
            line=dict(color='blue')
        )

        layout = go.Layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            )
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div')

    return render(request, 'graficas/grafica.html', {
        'plot_div': plot_div,
        'coordenadas': coordenadas.tolist()
    })

