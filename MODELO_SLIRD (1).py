# Importando las librerías necesarias
from dash import Dash, dcc, html, Input, Output  # Dash es para la creación de aplicaciones web interactivas.
import numpy as np  # Usado para crear y manejar arrays y cálculos numéricos.
from scipy.integrate import odeint  # Para resolver ecuaciones diferenciales.
import plotly.graph_objects as go  # Para crear gráficos interactivos.

# Es necesario instalar estas librerías antes de ejecutar el código:
# pip install dash
# pip install dcc
# pip install odeint
# pip install numpy
# pip install plotly


# Creamos la aplicación Dash
app = Dash(__name__)

# Definimos el modelo SLIRD (Susceptibles, Latentes, Infectados, Recuperados, Muertos).
def slird_model(y, t, beta, rho, delta, alpha, lambda_, gamma):
    S, L, I, R = y  # Desempaquetamos las variables de estado
    dSdt = alpha - beta * S * I + lambda_ * R  # Ecuación diferencial para los susceptibles
    dLdt = beta * S * I - gamma * L  # Ecuación diferencial para los latentes
    dIdt = gamma * L - delta * I - rho * I  # Ecuación diferencial para los infectados
    dRdt = rho * I - lambda_ * R  # Ecuación diferencial para los recuperados
    return [dSdt, dLdt, dIdt, dRdt]  # Retornamos las ecuaciones diferenciales

# Layout de la aplicación web
app.layout = html.Div(
    style={  # Estilo general del contenedor principal
        'font-family': 'Roboto, sans-serif',
        'background-color': '#f4f6f9',
        'color': '#333',
        'display': 'flex',
        'flexDirection': 'row', 
        'alignItems': 'center',
        'justifyContent': 'center',
        'height': '100vh',
        'padding': '0 20px'
    },
    children=[
        html.Div(
            style={  # Estilo del panel de entrada
                'backgroundColor': '#ffffff',
                'borderRadius': '15px',
                'padding': '30px',
                'boxShadow': '0 10px 20px rgba(0, 0, 0, 0.1)',
                'width': '100%',
                'maxWidth': '400px',
                'display': 'grid',
                'gap': '15px',
            },
            children=[
                html.H1(  # Título principal de la aplicación
                    "Modelo SLIRD Interactivo",
                    style={  # Estilo del título
                        'font-size': '24px',
                        'font-weight': '600',
                        'color': '#333',
                        'marginBottom': '20px',
                        'textAlign': 'center',
                        'font-family': 'Roboto, sans-serif',
                    }
                ),
                # Definimos las etiquetas y campos de entrada para los parámetros del modelo SLIRD
                html.Label("β (Tasa de contacto):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="beta", type="number", value=0.3, step=0.01, style={  # Entrada para β
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("ρ (Tasa de recuperación):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="rho", type="number", value=0.1, step=0.01, style={  # Entrada para ρ
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("δ (Tasa de mortalidad):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="delta", type="number", value=0.05, step=0.01, style={  # Entrada para δ
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("α (Ingreso de susceptibles):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="alpha", type="number", value=0.01, step=0.01, style={  # Entrada para α
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("λ (Reinfección):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="lambda", type="number", value=0.01, step=0.01, style={  # Entrada para λ
                    'width': '100%',
                    'padding': '12px',
                    'fontSize': '14px',
                    'borderRadius': '10px',
                    'border': '1px solid #ddd',
                    'backgroundColor': '#f9f9f9',
                    'color': '#333',
                }),
                html.Label("γ (Tasa de latente a infectado):", style={'fontSize': '14px', 'fontWeight': '500'}),
                dcc.Input(id="gamma", type="number", value=0.1, step=0.01, style={  # Entrada para γ
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
        html.Div(  # Contenedor para el gráfico
            style={  # Estilo del contenedor del gráfico
                'width': '100%',
                'maxWidth': '900px',
                'height': '600px', 
                'marginLeft': '30px'
            },
            children=[dcc.Graph(id="slird-graph")]  # Gráfico para mostrar los resultados
        ),
    ]
)

# Definimos el callback para actualizar el gráfico con los parámetros introducidos por el usuario
@app.callback(
    Output("slird-graph", "figure"),  # El gráfico se actualizará con el nuevo valor
    [Input("beta", "value"),
     Input("rho", "value"),
     Input("delta", "value"),
     Input("alpha", "value"),
     Input("lambda", "value"),
     Input("gamma", "value")]
)
def update_graph(beta, rho, delta, alpha, lambda_, gamma):
    # Condiciones iniciales
    S0, L0, I0, R0 = 0.99, 0.0, 0.01, 0.0
    y0 = [S0, L0, I0, R0]  # Inicializamos los valores del modelo
    t = np.linspace(0, 160, 160)  # Tiempo de simulación

    # Resolución de las ecuaciones diferenciales
    solution = odeint(slird_model, y0, t, args=(beta, rho, delta, alpha, lambda_, gamma))
    S, L, I, R = solution.T  # Transponemos para obtener cada componente

    # Creamos el gráfico con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles', line=dict(color='#1f77b4')))
    fig.add_trace(go.Scatter(x=t, y=L, mode='lines', name='Latentes', line=dict(color='#ff7f0e')))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados', line=dict(color='#d62728')))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados', line=dict(color='#2ca02c')))

    # Actualizamos el diseño del gráfico
    fig.update_layout(
        title='Modelo SLIRD',
        xaxis_title='Tiempo',
        yaxis_title='Proporción de la población',
        hovermode='x unified',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#f4f6f9',
        font=dict(family="Roboto, sans-serif", size=12, color="#333"),
        legend=dict(
            x=0.01, y=0.99, traceorder="normal",
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="Black", borderwidth=1
        )
    )

    return fig  # Devolvemos el gráfico actualizado

# Ejecutamos el servidor
if __name__ == "__main__":
    app.run_server(debug=True)

