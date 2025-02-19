import streamlit as st 
import base64
import time
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
#import seaborn as sns
import scipy.optimize as sco
from scipy import stats
import base64
import streamlit.components.v1 as components


import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")

# Configuración de Streamlit
st.set_page_config(page_title="Frontera Eficiencia-Modelo Montecarlo", page_icon="img/stock-market.png", layout="wide")
theme_plotly = None

#"""" codigo de particulas que se agregan en le background""""
particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    background-color: #191970;    
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  
</style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 300,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#fffc33"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "img/github.svg",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#fffc33",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""
globe_js = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vanta Globe Animation</title>
    <style type="text/css">
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        overflow: hidden;
        height: 100%;
        margin: 0;
        background-color: #1817ed; /* Fondo azul */
      }
      #canvas-globe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="canvas-globe"></div>       

    <!-- Scripts de Three.js y Vanta.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.globe.min.js"></script>

    <script type="text/javascript">      
      document.addEventListener("DOMContentLoaded", function() {
        VANTA.GLOBE({
          el: "#canvas-globe", // El elemento donde se renderiza la animación
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          minHeight: 200.00,
          minWidth: 200.00,
          scale: 1.00,
          scaleMobile: 1.00,
          color: 0xd1ff3f, // Color verde amarillento
          backgroundColor: 0x1817ed // Fondo azul
        });
      });
    </script>
  </body>
</html>
"""
waves_js = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vanta Waves Animation</title>
    <style type="text/css">
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      html, body {
        height: 100%;
        margin: 0;
        overflow: hidden;
      }
      #canvas-dots {
        position: absolute;
        width: 100%;
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="canvas-waves"></div>       
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.waves.min.js"></script>
    
    <script type="text/javascript">      
      document.addEventListener("DOMContentLoaded", function() {
        VANTA.WAVES({
          el: "#canvas-waves", // Especificar el contenedor donde debe renderizarse
           mouseControls: true,
           touchControls: true,
           gyroControls: false,
           minHeight: 200.00,
           minWidth: 200.00,
           scale: 1.00,
           scaleMobile: 1.00,
           color: 0x15159b
        });
      });
    </script>
  </body>
</html>
"""

#""" imagen de background"""
def add_local_background_image(image):
  with open(image, "rb") as image:
    encoded_string = base64.b64encode(image.read())
    st.markdown(
      f"""
      <style>
      .stApp{{
        background-image: url(data:files/{"jpg"};base64,{encoded_string.decode()});
      }}    
      </style>
      """,
      unsafe_allow_html=True
    )
add_local_background_image("img/fondo.jpg")

#""" imagen de sidebar"""
def add_local_sidebar_image(image):
  with open(image, "rb") as image:
    encoded_string = base64.b64encode(image.read())
    st.markdown(
      f"""
      <style>
      .stSidebar{{
        background-image: url(data:files/{"jpg"};base64,{encoded_string.decode()});
      }}    
      </style>
      """,
      unsafe_allow_html=True
    )

add_local_sidebar_image("img/fondo1.jpg")

with st.container():
    #st.write("---")
    left, midle ,right = st.columns(3, gap='small', vertical_alignment="center")
    with left:
        components.html(waves_js, height=100,scrolling=False)
    with midle:
        components.html(globe_js, height=100,scrolling=False) 
    with right:
       components.html(particles_js, height=100,scrolling=False) 
    #st.write("---")    


#-------------- animacion con css de los botones modelo Arima ------------------------
with open('style/style.css') as f:
        css = f.read()
        
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.logo(image="img/market.png",size='large')

st.button("Frontera de Eficiencia Modelo Montecarlo para Acitvos de EEUU", key="pulse", use_container_width=True)
st.warning('breve explicación de modelo montercarlo')
st.markdown(f"""¿Cómo funciona la simulación de Montecarlo? A diferencia de un modelo de pronóstico normal,
           la simulación de Montecarlo predice un conjunto de resultados basados en un rango estimado de valores
           frente a un conjunto de valores de entrada fijos. En otras palabras, una simulación de Montecarlo 
           construye un modelo de posibles resultados aprovechando una distribución de probabilidad, como una distribución uniforme o normal, 
           para cualquier variable que tenga incertidumbre inherente. A continuación, vuelve a calcular los resultados una y otra vez,
           utilizando cada vez un conjunto diferente de números aleatorios entre los valores mínimo y máximo. 
           En un experimento típico de Montecarlo, este ejercicio se puede repetir miles de veces para producir un gran número de resultados probables.
           Las simulaciones de Montecarlo también se utilizan para predicciones a largo plazo debido a su precisión.
           A medida que aumenta el número de entradas, también crece el número de pronósticos, lo que le permite proyectar los resultados
           más lejos en el tiempo con más precisión. Cuando se completa una simulación de Montecarlo, 
           arroja una serie de posibles resultados con la probabilidad de que se produzca cada resultado.

    """)
st.write('###')
#-------------------------desarrollo frontera de eficiencia modelo montercarlo --------------------
# Título principal

# Función para descargar datos históricos
def get_stock_data(tickers, start_date, end_date):
    data = pd.DataFrame()
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)['Close']
        data[ticker] = stock_data
    return data

# Entrada de datos por parte del usuario
with st.container(border=True):
    col1, col2,col3, col4 = st.columns(4, gap='small',vertical_alignment="top", border=True) 
    with col1:
        numero = int(st.number_input("Digite el número de acciones que componen el Portfolio", min_value=5, max_value=15, step=1, placeholder=5, help="Valor entre 5 y 15"))
    with col2:
        tickers_input = st.text_input(f"Ingrese {numero} tickers acciones/crypto (separados por comas)", "AAPL, BTC-USD, JNJ, JPM, NVDA").upper()
        tickers = [ticker.strip() for ticker in tickers_input.split(',')][:numero]
    with col3:
        start_date = st.date_input("Fecha de inicio", value=pd.to_datetime('2019-01-01'), help="Ingrese fecha que sea igual o menor a 10 años")
        end_date = st.date_input("Fecha de fin", value=pd.to_datetime('2025-03-01'), help="Puede colocar fecha superior a la fecha actual")
    with col4:
        rf_rate = float(st.number_input("Digite tasa de libre riesgo (en % ej. 4.5)", min_value=0.5, max_value=15.5, step=0.5, value=4.5, help="Ejemplo: 4.5% "))/100


st.write("###")

if st.button("Ejecutar Frontera de Eficiencia", key="glow-on-portfolio"):
      with st.status("Generando el modelo...", expanded=True) as status:
        st.write("Buscando datos...")
        time.sleep(2)
        st.write("Desplegando modelo.")
        time.sleep(1)
        st.write("Modelo finalizando...")
        time.sleep(1)
        status.update(
            label="Proceso completado!", state="complete", expanded=False
        ) 
    
      # Obtener datos del portafolio
      stock_data = get_stock_data(tickers, start_date, end_date)

      # Obtener datos de los índices
      indices_tickers = ['^DJI', 'SPY', '^IXIC']  # Dow Jones, S&P500, Nasdaq
      indices_data = get_stock_data(indices_tickers, start_date, end_date)

      # Calcular retornos diarios
      returns = stock_data.pct_change()  # Retornos simples
      indices_returns = indices_data.pct_change()

      # Simulación de Monte Carlo
      num_portfolios = 1000

      # Arrays para almacenar resultados
      all_weights = np.zeros((num_portfolios, len(tickers)))
      ret_arr = np.zeros(num_portfolios)
      vol_arr = np.zeros(num_portfolios)
      sharpe_arr = np.zeros(num_portfolios)

      # Simulación Monte Carlo
      for port in range(num_portfolios):
          # Generar pesos aleatorios
          weights = np.random.random(len(tickers))
          weights = weights/np.sum(weights)  # Normalización de pesos
          all_weights[port,:] = weights

          # Calcular retorno esperado
          port_ret = np.sum(returns.mean() * weights) * 252
          ret_arr[port] = port_ret

          # Calcular volatilidad del portafolio
          port_vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
          vol_arr[port] = port_vol

          # Calcular Ratio de Sharpe
          sharpe_arr[port] = (port_ret - rf_rate) / port_vol

      # Encontrar el portafolio óptimo (mayor Ratio de Sharpe)
      optimal_idx = sharpe_arr.argmax()
      optimal_weights = all_weights[optimal_idx,:]
      optimal_ret = ret_arr[optimal_idx]
      optimal_vol = vol_arr[optimal_idx]
      optimal_sharpe = sharpe_arr[optimal_idx]

      # Crear DataFrame con resultados
      results = pd.DataFrame({
          'Return': ret_arr,
          'Volatility': vol_arr,
          'Ratio de Sharpe': sharpe_arr
      })

      # Visualización de la frontera de eficiencia
      plt.figure(figsize=(15,6))
      plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis', marker='o', s=10)
      plt.colorbar(label='Ratio de Sharpe')
      plt.scatter(optimal_vol, optimal_ret, color='red', marker='*', s=200, label='Portfolio Óptimo')   
      plt.xlabel('Volatilidad')
      plt.ylabel('Retorno Esperado')    
      plt.title('Resultados de la optimización de cartera')
      plt.legend()   
      st.pyplot(plt)

      # Mostrar resultados del portafolio óptimo
      with st.container(border=True):
          col1, col2 = st.columns(2, gap='medium',vertical_alignment="top", border=True)  
          with col1:
              st.write(f"Tasa de libre riesgo: {rf_rate*100:.2f} % anual")
              st.write("---")
              st.write("\nInformación de Portafolio Óptimo:")      
              st.write(f"Retorno Esperado: {optimal_ret*100:.2f}% anual")
              st.write(f"Volatilidad: {optimal_vol*100:.2f}% anual")
              st.write(f"Ratio de Sharpe: {optimal_sharpe:.2f} % ")
          with col2:
              st.write("\nParticipación % óptima de acciones:")
              for stock, weight in zip(tickers, optimal_weights):
                  st.write(f"{stock}: {weight*100:.2f}%")

      # Calcular rendimiento acumulado del portafolio
      portfolio_value = (1 + returns.dot(optimal_weights)).cumprod()
      portfolio_return = (portfolio_value[-1] - 1) * 100

      # Calcular rendimiento acumulado del portafolio
      portfolio_value = (1 + returns.dot(optimal_weights)).cumprod()
      portfolio_return = (portfolio_value[-1] - 1) * 100

      # Calcular rendimiento acumulado de los índices
      indices_value = (1 + indices_returns).cumprod()
      indices_return = (indices_value.iloc[-1] - 1) * 100
      start_date_formatted = start_date.strftime('%d-%m-%Y')
      end_date_formatted = end_date.strftime('%d-%m-%Y')
      # Mostrar rendimiento comparativo en formato de subheader
      with st.container(border=True):
          st.write(f"\nRendimiento Acumulado del Portafolio vs Índices desde {start_date_formatted} hasta {end_date_formatted}")
          col1, col2 = st.columns(2, gap='medium',vertical_alignment="top", border=True)  
          with col1:    
              st.write(f"Rendimiento del Portafolio: {portfolio_return:.2f}%")
              st.write(f"Rendimiento Dow Jones: {indices_return['^DJI']:.2f}%")
          with col2:  
              st.write(f"Rendimiento S&P 500: {indices_return['SPY']:.2f}%")
              st.write(f"Rendimiento Nasdaq: {indices_return['^IXIC']:.2f}%")
      with st.expander("Gráfico de Ratio de Sharpe de los activos seleccinados"):
        st.warning("La ratio de Sharpe es un indicador utilizado para medir la rentabilidad que ofrece una inversión en relación al riesgo que se asume con ella. Su creador fue el economista estadounidense y premio Nobel de Economía William Forsyth Sharpe (Cambridge, Massachusetts, 1934).Usualmente, un inversor suele fijarse en la rentabilidad de un activo para decidir dónde colocar su dinero. Sin embargo, otra variable que hay que tener en cuenta al tomar esta decisión es el nivel de riesgo de cada inversión. En este sentido, la ratio de Sharpe mide el exceso de rendimiento por unidad de riesgo de una inversión y permite averiguar hasta qué punto la rentabilidad de una inversión compensa al inversor por el riesgo que asume.La ratio de Sharpe es una de las fórmulas que se utilizan para valorar un fondo de inversión. Es sencilla de calcular y además permite comparar varios fondos entre sí: aquel que tenga una ratio de Sharpe más elevada proporcionará una mayor rentabilidad para un mismo nivel de riesgo. Consecuentemente, será preferido por los inversores.")
            # Obtener datos del portafolio
        stock_data = get_stock_data(tickers, start_date, end_date)

        # Calcular retornos diarios
        returns = stock_data.pct_change()

        # Calcular Ratio de Sharpe de cada acción individualmente
        sharpe_ratios = {}
        for ticker in tickers:
            # Calcular retorno esperado y volatilidad para cada acción
            avg_return = returns[ticker].mean() * 252  # Retorno anualizado
            volatility = returns[ticker].std() * np.sqrt(252)  # Volatilidad anualizada
            sharpe_ratios[ticker] = (avg_return - rf_rate) / volatility  # Ratio de Sharpe

        # Visualizar el gráfico de barras para el Ratio de Sharpe de cada acción
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(sharpe_ratios.keys(), sharpe_ratios.values(), color='#9333ff')
        ax.set_xlabel('Acciones/Tickers')
        ax.set_ylabel('Ratio de Sharpe')
        ax.set_title('Ratio de Sharpe de cada acción en el Portafolio')
        st.pyplot(fig)  
    
st.write("###")   

# --------------- footer -----------------------------
st.write("---")
with st.container():
  #st.write("---")
  st.write("&copy; - derechos reservados -  2024 -  Walter Gómez - FullStack Developer - Data Science - Business Intelligence")
  #st.write("##")
  left, right = st.columns(2, gap='medium', vertical_alignment="bottom")
  with left:
    #st.write('##')
    st.link_button("Mi LinkedIn", "https://www.linkedin.com/in/walter-gomez-fullstack-developer-datascience-businessintelligence-finanzas-python/",use_container_width=True)
  with right: 
     #st.write('##') 
    st.link_button("Mi Porfolio", "https://walter-portfolio-animado.netlify.app/", use_container_width=True)
      
