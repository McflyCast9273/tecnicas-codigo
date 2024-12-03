# Importamos las librerías necesarias
from dash import Dash, dcc, html, Input, Output  # Dash para la interfaz y componentes interactivos
import numpy as np  # Para realizar cálculos y manejar datos numéricos
from scipy.integrate import odeint  # Para resolver ecuaciones diferenciales

# Es necesario instalar estas librerías antes de ejecutar el código:
# pip install dash
# pip install numpy
# pip install scipy

# Creamos la aplicación Dash
app = Dash(__name__)

# Definimos el modelo SIRD con ecuaciones diferenciales
def sird_model(y, t, beta, rho, delta, alpha, lambda_):
    S, I, R = y  # Variables: Susceptibles (S), Infectados (I), Recuperados (R)
    # Ecuaciones diferenciales para el modelo SIRD
    dSdt = alpha - beta * S * I + lambda_ * R  # Cambio en los susceptibles
    dIdt = beta * S * I - delta * I - rho * I  # Cambio en los infectados
    dRdt = rho * I - lambda_ * R  # Cambio en los recuperados
    return [dSdt, dIdt, dRdt]  # Retornamos las derivadas

# Definimos el diseño (layout) de la aplicación Dash
app.layout = html.Div(
    style={
        # Estilo general del diseño
        'font-family': 'Roboto, sans-serif',
        'background-color': '#f4f6f9',
        'color': '#333',
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
        'justifyContent': 'center',
        'height': '100vh',  # Altura completa de la ventana
        'padding': '0 20px'
    },
    children=[
        # Primer bloque: Controles para ajustar parámetros del modelo
        html.Div(
            style={
                'backgroundColor': '#ffffff',
                'borderRadius': '15px',
                'padding': '30px',
                'boxShadow': '0 10px 20px rgba(0, 0, 0, 0.1)',  # Sombra para dar profundidad
                'width': '100%',
                'maxWidth': '400px',
                'display': 'grid',
                'gap': '15px',
            },
            children=[
                html.H1(
                    "AJUSTE DE VALORES",  # Título del bloque
                    style={
                        'font-size': '24px',
                        'font-weight': '600',
                        'color': '#333',
                        'marginBottom': '20px',
                        'textAlign': 'center'
                    }
                ),
                # Campos de entrada para cada parámetro del modelo
                html.Label("β (Tasa de contacto):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="beta", type="number", value=0.3, step=0.01, style={
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("ρ (Tasa de recuperación):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="rho", type="number", value=0.1, step=0.01, style={
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("δ (Tasa de mortalidad):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="delta", type="number", value=0.05, step=0.01, style={
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("α (Ingreso de susceptibles):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="alpha", type="number", value=0.01, step=0.01, style={
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("λ (Reinfección):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="lambda", type="number", value=0.01, step=0.01, style={
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
            ]
        ),
        # Segundo bloque: Gráfica del modelo SIRD
        html.Div(
            style={
                'width': '100%',
                'maxWidth': '1000px',
                'height': '600px',  # Tamaño del área gráfica
                'marginLeft': '30px'
            },
            children=[dcc.Graph(id="sird-graph")]  # Gráfica generada por Dash
        ),
    ]
)

# Función de actualización para la gráfica
@app.callback(
    Output("sird-graph", "figure"),
    [Input("beta", "value"),
     Input("rho", "value"),
     Input("delta", "value"),
     Input("alpha", "value"),
     Input("lambda", "value")]
)
def update_graph(beta, rho, delta, alpha, lambda_):
    # Condiciones iniciales del modelo
    S0, I0, R0 = 0.99, 0.01, 0.0  # Población inicial: 99% susceptible, 1% infectada
    y0 = [S0, I0, R0]  # Vector de condiciones iniciales
    t = np.linspace(0, 160, 160)  # Tiempo de simulación (160 días)

    # Resolución de las ecuaciones diferenciales
    solution = odeint(sird_model, y0, t, args=(beta, rho, delta, alpha, lambda_))
    S, I, R = solution.T  # Extraemos los resultados: S, I, R

    # Configuración de la gráfica
    fig = {
        "data": [
            {"x": t, "y": S, "type": "line", "name": "Susceptibles", "line": {"color": "#1f77b4"}},
            {"x": t, "y": I, "type": "line", "name": "Infectados", "line": {"color": "#ff7f0e"}},
            {"x": t, "y": R, "type": "line", "name": "Recuperados", "line": {"color": "#2ca02c"}},
        ],
        "layout": {
            "title": "Modelo SIRD",  # Título de la gráfica
            "xaxis": {"title": "Tiempo"},
            "yaxis": {"title": "Proporción de la población"},
            'plot_bgcolor': '#ffffff',
            'paper_bgcolor': '#f4f6f9',
        },
    }
    return fig  # Retornamos la gráfica actualizada

# Ejecutamos la aplicación en el host local
if __name__ == "__main__":
    app.run_server(debug=True, host='localhost', port=8050)