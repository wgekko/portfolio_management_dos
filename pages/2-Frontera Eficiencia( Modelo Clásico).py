import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import yfinance as yf  
import seaborn as sns
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions
from pypfopt import plotting
from pypfopt import HRPOpt

import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")

# Configuración de Streamlit
st.set_page_config(page_title="Frontera Eficiencia-Modelo Clasico", page_icon="img/stock-market.png", layout="wide")
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

st.button("Frontera de Eficiencia Modelo Clásico para Activos de EEUU", key="pulse", use_container_width=True)
st.warning('La frontera eficiente parte del análisis de un portafolio o cartera de inversión y busca identificar cuáles son las inversiones más rentables y menos riesgosas que lo componen. Se basa en el principio básico de que el inversionista, mediante la diversificación, busque maximizar los rendimientos de su cartera con el menor riesgo posible.\n En esencia, la frontera eficiente busca identificar mediante una representación virtual, cuál es la mejor combinación de activos que brindará los mejores y menos volátiles rendimientos en el tiempo.')
st.write('###')
#-------------------------desarrollo  --------------------
# Título principal
st.title('Optimización de Portfolio con Frontera Eficiente')

# Entrada de datos por parte del usuario
with st.container(border=True):
    col1, col2,col3 = st.columns(3, gap='small',vertical_alignment="top", border=True) 
    with col1:
        start_date = st.date_input('Fecha de inicio', value=pd.to_datetime('2021-01-01'))
        end_date = st.date_input('Fecha de fin', value=pd.to_datetime('2025-02-17'))        
    with col2:
        stocks_input = st.text_input('Ingresa los símbolos de las acciones (separados por coma)', 'AAPL,BTC-USD,INTC,AMD,NVDA')
        stocks = stocks_input.split(",") # eliminamos los espacios luego de la coma
    with col3:
        risk_free_rate = st.number_input('Ingresa la tasa de libre riesgo (por ejemplo 2%)', value=4.5)/100

st.write("###")        
if st.button("Ejecutar Frontera Eficiente", key="btn-wobble"):
#if st.button("Ejecutar Frontera de Eficiencia", key="glow-on-port"):
       # Validar el número de acciones
    if len(stocks) < 3 or len(stocks) > 10:
          st.error("Error: El número de acciones debe ser entre 3 y 10.")
    else:
          # Descargar los datos de las acciones
          df = yf.download(stocks, start=start_date, end=end_date, rounding=True)

    with st.container(border=True):
        # Calcular precios y rendimientos
        precios = df['Close']
        rendimientos = precios.pct_change()[1:]
        rendEsp = rendimientos.mean()
        # Rendimiento esperado
        rendEsp1 = expected_returns.mean_historical_return(precios, returns_data=False, compounding=True, frequency=252, log_returns=False)
        col1, col2 = st.columns(2, gap='small',vertical_alignment="top", border=True) 
        with col1:  
            # Mostrar gráfico del rendimiento esperado
            st.subheader('Rendimiento Esperado (Histórico-anual)')
            for stock, value in rendEsp1.items():
                st.write(f"{stock} : {value * 100:.2f}%")
               # Gráfico de rendimiento esperado histórico (barras verticales)
            fig, ax = plt.subplots()
            rendEsp1.plot(kind="bar", ax=ax)
            ax.set_ylabel('Rendimiento Esperado(%)')  # Etiqueta eje Y
            ax.set_xlabel('Acciones')  # Etiqueta eje X
            st.pyplot(fig)
        with col2:  
            # Otros cálculos de rendimiento
            rendEsp2 = expected_returns.ema_historical_return(precios, returns_data=False, compounding=True, span=500, frequency=252, log_returns=False)
            st.subheader('Rendimiento Esperado (EMA-anual)')
            for stock, value in rendEsp2.items():
                st.write(f"{stock} : {value * 100:.2f}%")
            # Gráfico de rendimiento esperado EMA (barras verticales)
            fig2, ax2 = plt.subplots()
            rendEsp2.plot(kind="bar", ax=ax2)
            ax2.set_ylabel('Rendimiento Esperado(%)')  # Etiqueta eje Y
            ax2.set_xlabel('Acciones')  # Etiqueta eje X
            st.pyplot(fig2)     
         
            # Rendimiento esperado por CAPM
            rendEsp3 = expected_returns.capm_return(precios, market_prices=None, returns_data=False, risk_free_rate=risk_free_rate, compounding=True, frequency=252, log_returns=False)
                
    with st.container(border=True):
        st.subheader("Matrices de Covarianza")
        st.write("""
            **Matriz de Covarianza Simple:**
            Esta matriz muestra la covarianza directa entre los activos, basada en los rendimientos históricos.
             **Matriz de Covarianza Ajustada (Ledoit-Wolf):**
            Este es un ajuste de la covarianza simple utilizando el método de shrinkage Ledoit-Wolf. Este ajuste mejora la precisión cuando el número de activos es pequeño, reduciendo la sobreestimación de la varianza.
            """)  
        col1, col2 = st.columns(2, gap='small',vertical_alignment="top", border=True) 
        with col1:
            # Matriz de covarianza
            matrizCov = rendimientos.cov()
            matrizCov1 = risk_models.sample_cov(precios)

            # Mostrar matriz de covarianza simple
            st.write('Covarianza de Activos (Simple)')
            fig18, ax18 = plt.subplots(figsize=(12, 8))
            sns.heatmap(matrizCov1, ax=ax18, fmt=".2f", annot=True)
            ax18.set_title('Matriz de Covarianza Simple: Covarianza entre los activos', fontsize=14)
            st.pyplot(fig18)
               
        with col2:
            matrizCov2 = risk_models.CovarianceShrinkage(precios).ledoit_wolf()
            # Mostrar matriz de covarianza ajustada con Ledoit-Wolf
            st.write('Covarianza de Activos (Ajustada-Ledoit-Wolf)')
            fig19, ax19 = plt.subplots(figsize=(12, 8))
            sns.heatmap(matrizCov2, ax=ax19, fmt=".2f", annot=True)
            ax19.set_title('Matriz de Covarianza Ajustada (Ledoit-Wolf)', fontsize=14)
            st.pyplot(fig19)
    with st.container(border=True): 
        st.subheader("Frontera Eficiencia-Volatilidad Mínima")
        # Frontera eficiente - mínima volatilidad
        col1, col2 = st.columns(2, gap='small',vertical_alignment="top", border=True) 
        with col1:
            fe = EfficientFrontier(rendEsp1, matrizCov2, weight_bounds=(0, 1))
            fe.min_volatility()
            pesos = fe.clean_weights()
            st.markdown('Porcentaje de partición del Portfolio-Mínima Volatilidad')
            # Filtrar pesos no nulos antes de graficar
            pesos = {k: v for k, v in pesos.items() if v > 0}            
            # Mostrar los pesos como porcentaje en el gráfico de torta
            fig3, ax3 = plt.subplots()
            pd.Series(pesos).plot(kind="pie", figsize=(6,6), ax=ax3, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig3)     
        with col2:
            fe.portfolio_performance(verbose=True)
            # Mostrar resultados adicionales de la cartera mínima volatilidad
            rendimiento, volatilidad, sharpe_ratio = fe.portfolio_performance()
            st.subheader('Resultados de Protfolio-Volatilidad Mínima')
            st.subheader(f"**Rendimiento anual esperado**: {rendimiento*100:.2f}%")
            st.subheader(f"**Volatilidad anual**: {volatilidad*100:.2f}%")
            st.subheader(f"**Ratio de Sharpe**: {sharpe_ratio:.2f}")

    with st.container(border=True): 
        st.subheader("Frontera Eficiencia-Máximo Ratio Sharpe") 
        # Frontera eficiente - máximo Sharpe
        col1, col2 = st.columns(2, gap='small',vertical_alignment="top", border=True) 
        with col1:
            fe = EfficientFrontier(rendEsp1, matrizCov2, weight_bounds=(0, 1))  # Nueva instancia antes de resolver
            fe.max_sharpe(risk_free_rate=risk_free_rate)
            pesos = fe.clean_weights()
            st.markdown('Porcentaje de partición del Portfolio-Máximo Sharpe')
            # Filtrar pesos no nulos antes de graficar
            pesos = {k: v for k, v in pesos.items() if v > 0}            
            # Mostrar los pesos como porcentaje en el gráfico de torta
            fig4, ax4 = plt.subplots()
            pd.Series(pesos).plot(kind="pie", figsize=(6,6), ax=ax4, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig4)
            fe.portfolio_performance(verbose=True)
        with col2:
            # Mostrar resultados adicionales de la cartera máximo Sharpe
            rendimiento, volatilidad, sharpe_ratio = fe.portfolio_performance()
            st.subheader('Resultados de Portfolio-Máximo Sharpe')
            st.subheader(f"**Rendimiento anual esperado**: {rendimiento*100:.2f}%")
            st.subheader(f"**Volatilidad anual**: {volatilidad*100:.2f}%")
            st.subheader(f"**Ratio de Sharpe**: {sharpe_ratio:.2f}")
            
    with st.container(border=True): 
        st.subheader("Frontera Eficiencia-Riesgo Eficiente") 
        # Frontera eficiente - riesgo eficiente
        col1, col2 = st.columns(2, gap='small',vertical_alignment="top", border=True) 
        with col1:
            fe = EfficientFrontier(rendEsp1, matrizCov2)  # Nueva instancia antes de resolver
            fe.efficient_risk(target_volatility=0.25)
            pesos = fe.clean_weights() 
            st.markdown('Porcentaje de partición del Portfolio-Riesgo Eficiente')
            # Filtrar pesos no nulos antes de graficar
            pesos = {k: v for k, v in pesos.items() if v > 0}            
            # Mostrar los pesos como porcentaje en el gráfico de torta
            fig5, ax5 = plt.subplots()
            pd.Series(pesos).plot(kind="pie", figsize=(6,6), ax=ax5, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig5)
            fe.portfolio_performance(verbose=True)
        with col2:
            # Mostrar resultados adicionales de la cartera riesgo eficiente
            rendimiento, volatilidad, sharpe_ratio = fe.portfolio_performance()
            st.subheader('Resultados del Portfolio-Riesgo Eficiente')
            st.subheader(f"**Rendimiento anual esperado**: {rendimiento*100:.2f}%")
            st.subheader(f"**Volatilidad anual**: {volatilidad*100:.2f}%")
            st.subheader(f"**Ratio de Sharpe**: {sharpe_ratio:.2f}")

    with st.container(border=True):
        st.subheader("Frontera Eficiencia-Rendimiento Eficiente")
        # Frontera eficiente - retorno eficiente
        col1, col2 = st.columns(2, gap='small',vertical_alignment="top", border=True) 
        with col1:        
            fe = EfficientFrontier(rendEsp1, matrizCov2)  # Nueva instancia antes de resolver
            fe.efficient_return(target_return=0.35)
            pesos = fe.clean_weights()      
            st.markdown('Porcentaje de partición del Portfolio-Retorno Eficiente')
            # Filtrar pesos no nulos antes de graficar
            pesos = {k: v for k, v in pesos.items() if v > 0}            
            # Mostrar los pesos como porcentaje en el gráfico de torta
            fig6, ax6 = plt.subplots()
            pd.Series(pesos).plot(kind="pie", figsize=(6,6), ax=ax6, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig6)
            fe.portfolio_performance(verbose=True)
        with col2:    
            # Mostrar resultados adicionales de la cartera retorno eficiente
            rendimiento, volatilidad, sharpe_ratio = fe.portfolio_performance()
            st.subheader('Resultados del Portfolio-Retorno Eficiente')
            st.subheader(f"**Rendimiento anual esperado**: {rendimiento*100:.2f}%")
            st.subheader(f"**Volatilidad anual**: {volatilidad*100:.2f}%")
            st.subheader(f"**Ratio de Sharpe**: {sharpe_ratio:.2f}")

    with st.container(border=True):
        st.subheader("Frontera Eficiencia-Optimización HRP")
        st.warning("La optimización de carteras de instrumentos financieros es una tarea que se lleva a cabo todos los días en los mercados financieros. Para ello, generalmente se utiliza un enfoque matemático conocido como optimización cuadrática, \n diseñado para resolver problemas de optimización de carteras que incluyen restricciones de desigualdad. Un algoritmo comúnmente utilizado para esto es el Critical Line Algorithm (CLA), que garantiza encontrar una solución exacta tras varias iteraciones. \n Sin embargo, aunque la metodología matemática es adecuada, el CLA puede generar soluciones inestables debido a su enfoque en unos pocos activos de la cartera, lo que a menudo reduce su rendimiento fuera de la muestra. \n Esta inestabilidad se debe a que la optimización depende de la inversión en la matriz de covarianza, la cual se vuelve más difícil de manejar cuando los activos están altamente correlacionados, un escenario muy común en los mercados financieros.Marcos López de Prado (2016) propone una alternativa a este problema a través de la metodología Hierarchical Risk Parity (HRP), \n que utiliza técnicas de Machine Learning y teoría de grafos para crear un portafolio más equilibrado y diversificado basándose en la información contenida en la matriz de covarianza de los activos. HRP emplea un enfoque de clustering jerárquico, agrupando activos que comparten características similares. \n En el estudio, se analizan las acciones de las empresas que componen el índice S&P 500 entre 2015 y 2020. Se construye una cartera utilizando diferentes algoritmos de optimización y luego se comparan las asignaciones y los resultados de desempeño de cada uno. Además, se crean 11 portafolios que corresponden a los sectores en los que se divide el S&P 500 y se repite el análisis comparativo para cada uno de ellos. Para evaluar la estabilidad de las soluciones, también se realiza una simulación de Monte Carlo con variables aleatorias. Los principales hallazgos del análisis indican que el CLA tiende a concentrar las asignaciones en un pequeño número de activos (10 de un total de 34), mientras que el HRP distribuye las inversiones de manera más uniforme a lo largo del portafolio. Además, el HRP ofrece una mejor eficiencia de retorno ajustada por riesgo (medida por el ratio de Sharpe) en comparación con el CLA. Lo mismo ocurre en la simulación de Monte Carlo, que también muestra una mejor estabilidad en el HRP frente a posibles choques en los mercados. En resumen, el CLA muestra un rendimiento penalizado por su concentración en unos pocos activos, mientras que el HRP brinda una mayor protección en situaciones de incertidumbre al equilibrar la diversificación tanto en los activos individuales como en los grupos jerárquicos de activos.")
            # Optimización HRP
        col1, col2 = st.columns(2, gap='small',vertical_alignment="top", border=True) 
        with col1:       
            hrp = HRPOpt(rendimientos)
            hrp.optimize()
            pesos = hrp.clean_weights()
            st.markdown('Porcentaje de partición del Portfolio-Optimización HRP')
            st.warning("Es una técnica que combina la estructura jerárquica que existe entre los activos y la paridad de riesgo ingenua (pesos proporcionales a la inversa del riesgo).")
            # Mostrar rendimiento esperado y volatilidad para la optimización HRP
            rendimiento, volatilidad, _ = hrp.portfolio_performance()
            st.write('Resultados del Portfolio-Optimización HRP')
            st.write(f"**Rendimiento anual esperado**: {rendimiento*100:.2f}%")
            st.write(f"**Volatilidad anual**: {volatilidad*100:.2f}%")
            # Filtrar pesos no nulos antes de graficar
            pesos = {k: v for k, v in pesos.items() if v > 0}            
            # Mostrar los pesos como porcentaje en el gráfico de torta
            fig7, ax7 = plt.subplots()
            pd.Series(pesos).plot(kind="pie", figsize=(6,6), ax=ax7, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig7)
            hrp.portfolio_performance(verbose=True)
            
        with col2:   
            # Dendrograma HRP
            st.subheader('Dendrograma HRP')
            st.warning("El diagrama muestra las distancias entre clases fusionadas secuencialmente, evitando el cruce de líneas mediante un orden gráfico que ubica a los pares de clases cercanas como vecinos. La herramienta Dendrograma emplea un algoritmo de clustering jerárquico: calcula las distancias entre clases, fusiona iterativamente los pares más cercanos y actualiza las distancias después de cada fusión hasta fusionar todas las clases. Las distancias de fusión se usan para construir el dendrograma..")
            fig8, ax8 = plt.subplots(figsize=(10, 10))  # Mejorar el tamaño de la figura
            plotting.plot_dendrogram(hrp, ax=ax8, color_threshold=0.7)  # Mejorar el dendrograma
            st.pyplot(fig8)

    with st.container(border=True):
        st.subheader("Frontera Eficiencia-Diversificación")
        # Agregar objetivos de diversificación
        col1, col2 = st.columns(2, gap='small',vertical_alignment="center", border=True) 
        with col1:           
            fe = EfficientFrontier(rendEsp1, matrizCov2)  # Crear una nueva instancia
            fe.add_objective(objective_functions.L2_reg, gamma=0.1)
            fe.efficient_risk(target_volatility=0.25)
            pesos = fe.clean_weights() 
            st.subheader('Porcentaje de partición del Portfolio-Diversificado')
            # Filtrar pesos no nulos antes de graficar
            pesos = {k: v for k, v in pesos.items() if v > 0}            
            # Mostrar los pesos como porcentaje en el gráfico de torta
            fig9, ax9 = plt.subplots()
            pd.Series(pesos).plot(kind="pie", figsize=(6,6), ax=ax9, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig9)
            fe.portfolio_performance(verbose=True)
        with col2:   
            # Mostrar rendimiento, volatilidad y ratio de Sharpe
            rendimiento, volatilidad, sharpe_ratio = fe.portfolio_performance()
            st.subheader(f"**Rendimiento anual esperado**: {rendimiento*100:.2f}%")
            st.subheader(f"**Volatilidad anual**: {volatilidad*100:.2f}%")
            st.subheader(f"**Ratio de Sharpe**: {sharpe_ratio:.2f}")            
            # Frontera eficiente
            st.subheader('Frontera Eficiente')
            fe = EfficientFrontier(rendEsp1, matrizCov2)  # Nueva instancia antes de la llamada a plot
            fig10, ax10 = plt.subplots()
            plotting.plot_efficient_frontier(fe, show_assets=False, ax=ax10)
            # Generación de carteras aleatorias
            n_carteras = 10000
            w = np.random.dirichlet(np.ones(len(precios.columns)), n_carteras)
            rendimiento = w.dot(rendEsp1)
            riesgo = np.sqrt(np.diag(w @ matrizCov2 @ w.T))
            sharpes = rendimiento / riesgo
            ax10.scatter(riesgo, rendimiento, marker=".", c=sharpes, cmap="viridis_r")
            # Cartera de tangencia
            fe = EfficientFrontier(rendEsp1, matrizCov2)  # Nueva instancia antes de resolver
            fe.max_sharpe()
            rend_tangente, riesgo_tangente, _ = fe.portfolio_performance()
            ax10.scatter(riesgo_tangente, rend_tangente, marker="*", s=200, c="r", label="Portfolio")
            ax10.set_title("Frontera eficiente de Portfolio")
            ax10.legend()
            ax10.set_ylabel("Rendimiento Esperado")
            ax10.set_xlabel("Riesgo (volatilidad)")
            st.pyplot(fig10)

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
      
    