import streamlit as st 
import base64
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pypfopt import DiscreteAllocation
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns




import json
import streamlit.components.v1 as components



import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")

# Configuración de Streamlit
st.set_page_config(page_title="Frontera Eficiencia-Ponderador Portfolio", page_icon="img/stock-market.png", layout="wide")
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

st.button("Ponderar activos financieros de EEUU para un Portfolio", key="pulse", use_container_width=True)
st.warning('tener que considerar que al invertir en criptomonedas lo hace por el valor total no por facciones (caso criptomonedas)')
st.write('###')
#-------------------------desarrollo  --------------------
# Título principal
# Entrada de datos por parte del usuario
with st.container(border=True):
    col1, col2, col3 = st.columns(3, gap='small', vertical_alignment="top", border=True) 
with col1:
    # Solicitar al usuario la tasa libre de riesgo
    risk_free_rate = float(st.number_input("Ingrese la tasa libre de riesgo (ejemplo 4.5 %): ", value=4.5 ,key="risk_free_rate_input"))/100
with col2:
    investment = st.number_input("Ingrese el monto a invertir ($):", min_value=100, value=25000)
with col3:
    tickers_input = st.text_area("Ingrese los tickers separados por coma (mínimo 3, máximo 10):", 
                            value="BUD, XOM, BA, CHTR, SHOP, NVDA, WMT", help="minimo 3 y m+aximo 10 ticker de acciones")
    tickers = [ticker.strip() for ticker in tickers_input.split(",")]

    if len(tickers) < 3 or len(tickers) > 10:
        st.error("Debe ingresar entre 3 y 10 tickers.")
        st.stop()

st.write("###")

if st.button("Ejecutar Ponderador Portfolio", key="glitch"):
#if st.button("Ejecutar Ponderador de Portfolio", key="glow-on-reg"):
  
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_columns', None)

        def fetch_stock_data(tickers):
            stocks_prices = pd.DataFrame()

            for ticker in tickers:
                st.write(f"Obteniendo datos de {ticker}...")

                yticker = yf.Ticker(ticker)
                try:
                    # Obtener datos históricos
                    historyPrices = yticker.history(period='max')

                    # Asegurar que el índice sea un DatetimeIndex
                    if not isinstance(historyPrices.index, pd.DatetimeIndex):
                        historyPrices.index = pd.to_datetime(historyPrices.index)

                    # Agregar columnas Ticker, Año, Mes, Día de la semana, Fecha
                    historyPrices['Ticker'] = ticker
                    historyPrices['Year'] = historyPrices.index.year
                    historyPrices['Month'] = historyPrices.index.month
                    historyPrices['Weekday'] = historyPrices.index.weekday
                    historyPrices['Date'] = historyPrices.index.date

                    # Cálculo de rendimientos históricos
                    for i in [1, 3, 7, 30, 90, 365]:
                        historyPrices[f'growth_{i}d'] = historyPrices['Close'] / historyPrices['Close'].shift(i)

                    # Crecimiento futuro 3 días
                    historyPrices['future_growth_3d'] = historyPrices['Close'].shift(-3) / historyPrices['Close']

                    # Volatilidad en los últimos 30 días
                    historyPrices['volatility'] = historyPrices['Close'].rolling(30).std() * np.sqrt(252)

                    # Concatenar a el dataframe principal
                    stocks_prices = pd.concat([stocks_prices, historyPrices], ignore_index=True)

                except Exception as e:
                    st.write(f"Error al obtener datos de {ticker}: {e}")
                    continue  # Continuar con el siguiente ticker si hay un error

            return stocks_prices


        def plot_correlation_heatmap(stocks_prices):
            # Asegurar que la columna 'Date' esté en formato datetime
            stocks_prices['Date'] = pd.to_datetime(stocks_prices['Date'])

            # Pivotar los datos para tener 'Date' como índice, 'Ticker' como columnas y 'Close' como valores
            #df_pivot = stocks_prices.pivot(index='Date', columns='Ticker', values='Close').reset_index()
            df_pivot = stocks_prices.pivot(index='Date', columns='Ticker', values='Close')

            # Calcular la matriz de correlación
            corr = df_pivot.corr()

            # Crear figura y eje explícitamente
            fig, ax = plt.subplots() #figsize=(10, 4)
            fig.set_size_inches(8,6)
            # Graficar el heatmap de correlación
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, vmax=.3, square=True, annot=True, cmap='RdYlGn', ax=ax, fmt=".2f")
            ax.set_title("Mapa de Correlación de Acciones")
            # Pasar la figura a st.pyplot
            st.pyplot(fig)  # Renderizar gráfico en Streamlit


        def optimize_portfolio(df_pivot, risk_free_rate):
            mu = expected_returns.capm_return(df_pivot.set_index('Date'))
            S = risk_models.CovarianceShrinkage(df_pivot.set_index('Date')).ledoit_wolf()

            # Optimización de mínima volatilidad
            ef_min_vol = EfficientFrontier(mu, S, weight_bounds=(0, 1))
            ef_min_vol.min_volatility()
            weights_min_volatility = ef_min_vol.clean_weights()
            
            # Optimización de máxima relación Sharpe
            ef_max_sharpe = EfficientFrontier(mu, S, weight_bounds=(0, 1))
            ef_max_sharpe.max_sharpe()
            weights_max_sharpe = ef_max_sharpe.clean_weights()

            # Retorna todos los valores necesarios
            return weights_min_volatility, weights_max_sharpe, ef_min_vol, ef_max_sharpe

        def perform_discrete_allocation(weights_max_sharpe, df_pivot, investment):
            # Tomamos los precios más recientes (última fila)
            latest_prices = df_pivot.set_index('Date').iloc[-1]

            # Asegurarnos de que latest_prices no tenga valores NaN
            latest_prices = latest_prices.dropna()

            # Verificar que los tickers en los precios más recientes coincidan con los tickers en weights_max_sharpe
            matching_tickers = [ticker for ticker in weights_max_sharpe.keys() if ticker in latest_prices.index]

            if len(matching_tickers) != len(weights_max_sharpe):
                st.error("El precio de los activos seleccionados no pueden asignarse a los fondos que se desea invertir.")
                st.stop()

            # Crear un diccionario con los precios más recientes solo para los tickers que coinciden
            latest_prices = latest_prices[matching_tickers]

            # Realizar la asignación discreta
            da = DiscreteAllocation(weights_max_sharpe, latest_prices, total_portfolio_value=investment, short_ratio=0.0)

            try:
                alloc, leftover = da.lp_portfolio()
            except ValueError as e:
                st.error(f"Error al realizar la asignación discreta: {e}")
                st.stop()

            # Mostrar la asignación discreta en formato tabla
            alloc_df = pd.DataFrame(list(alloc.items()), columns=["Ticker", "Cantidad"])
            alloc_df["Porcentaje Asignado"] = alloc_df["Cantidad"] / alloc_df["Cantidad"].sum() * 100
            alloc_df["Valor Asignado"] = alloc_df["Cantidad"] * latest_prices[alloc_df["Ticker"]].values
            alloc_df["Valor Restante"] = leftover

            st.subheader(f"Asignación discreta para la inversión inicial de :  {investment}   - realizada con  saldo :  {leftover:.2f}  - restante.")
            st.table(alloc_df)  # Mostrar la asignación como tabla

            return alloc
        # Lógica principal
        stocks_prices = fetch_stock_data(tickers)
        # Graficar el mapa de correlación
        with st.container(border=True):
          st.subheader(" - Mapa de Correlación de Portfolio - ")
          plot_correlation_heatmap(stocks_prices)

        # Optimización de portafolio
        df_pivot = stocks_prices.pivot(index='Date', columns='Ticker', values='Close').reset_index()
          
        weights_min_volatility, weights_max_sharpe, ef_min_vol, ef_max_sharpe = optimize_portfolio(df_pivot, risk_free_rate)

        # Asignación discreta
        alloc = perform_discrete_allocation(weights_max_sharpe, df_pivot, investment)      
        # Mostrar asignación      
        with st.container(border=True):
            st.subheader("Optimización de mínima volatilidad (riesgo de Portfolio)")
            col1, col2 = st.columns(2, gap='small', vertical_alignment="top", border=True) 
            # Mostrar los resultados de la optimización de mínima volatilidad         
            with col1:  
              st.write("Ponderación '%' del portafolio para optimización de mínima volatilidad:")
              st.json({k: round(v*100, 2) for k, v in weights_min_volatility.items()})
            with col2:
              # Si necesitas el rendimiento y otras métricas, asegúrate de acceder a 'ef_min_vol' y 'ef_max_sharpe' correctamente
              expected_return_min_vol, volatility_min_vol, sharpe_min_vol = ef_min_vol.portfolio_performance(verbose=True, risk_free_rate=risk_free_rate)
              st.markdown(f'<p style="font-size:20px; background-color:#1a075a">&nbsp # Rendimiento anual esperado (mínima volatilidad): {expected_return_min_vol*100:.2f}%</p>',unsafe_allow_html=True)
              st.markdown(f'<p style="font-size:20px; background-color:#1a075a">&nbsp # Volatilidad anual (mínima volatilidad): {volatility_min_vol*100:.2f}%</p>',unsafe_allow_html=True)
              st.markdown(f'<p style="font-size:20px; background-color:#1a075a">&nbsp # Ratio de Sharpe (mínima volatilidad): {sharpe_min_vol:.2f}</p>',unsafe_allow_html=True)
              # Mostrar los resultados de la optimización de máxima relación Sharpe
        with st.container(border=True):
            st.subheader("Optimización de máxima relación Sharpe (rendimiento esperado)")
            col1, col2 = st.columns(2, gap='small', vertical_alignment="top", border=True)       
          
            with col1:
                st.write("Ponderación '%' del portafolio para optimización de máxima relación Sharpe:")
                st.json({k: round(v*100, 2) for k, v in weights_max_sharpe.items()})
            with col2:     
                # Resultados de la optimización de máxima relación Sharpe
                expected_return_max_sharpe, volatility_max_sharpe, sharpe_max_sharpe = ef_max_sharpe.portfolio_performance(verbose=True, risk_free_rate=risk_free_rate)
                st.markdown(f'<p style="font-size:20px; background-color:#1a075a">&nbsp # Rendimiento anual esperado (máxima relación Sharpe): {expected_return_max_sharpe*100:.2f}% </p>',unsafe_allow_html=True)
                st.markdown(f'<p style="font-size:20px; background-color:#1a075a">&nbsp # Volatilidad anual (máxima relación Sharpe): {volatility_max_sharpe*100:.2f}% </p>',unsafe_allow_html=True)
                st.markdown(f'<p style="font-size:20px; background-color:#1a075a">&nbsp # Ratio de Sharpe (máxima relación Sharpe): {sharpe_max_sharpe:.2f} </p>',unsafe_allow_html=True)

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
      
