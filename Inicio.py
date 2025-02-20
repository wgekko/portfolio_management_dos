import streamlit as st
import base64
import streamlit.components.v1 as components
from streamlit_multi_menu import streamlit_multi_menu
from datetime import datetime, timedelta

import warnings
warnings.simplefilter("ignore", category=FutureWarning)
# Suprimir advertencias ValueWarning
warnings.simplefilter("ignore")


# Configuración de Streamlit
st.set_page_config(page_title="Dashboard Portfolio Management", page_icon="img/stock.png", layout="wide")

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

# Agregar imágenes
# ---- animación de inicio de pagina----
with st.container():
    #st.write("---")
    left, midle ,right = st.columns(3, gap='small', vertical_alignment="center")
    with left:
        components.html(waves_js, height=120,scrolling=False)
    with midle:
        components.html(globe_js, height=120,scrolling=False) 
    with right:
       components.html(particles_js, height=120,scrolling=False) 
    #st.write("---")    
#-------------- animacion con css de los botones  ------------------------
with open('style/style.css') as f:
        css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if st.container(border=True):
  col1,col2,col3 = st.columns(3, gap='medium' ,vertical_alignment='center' )
  # Set up input widgets
  with col1:
    st.logo(image="img/logo3.png",size='large')
  with col2:
    st.logo(image="img/stock-market.png",size='large')
  with col3:
    st.logo(image="img/market.png",size='large')


# Título principal
st.button("Portfolio Management- Frontera Eficiencia-Ponderador de Inversión" , key="pulse", use_container_width=True)
#st.write('###')
# Parámetros de la barra lateral

with st.container():
    st.write("---")
    st.write('###')
    left, right = st.columns(2, gap='small', vertical_alignment="center")
    with left:
        st.button("Análsis de Activos Financieros para un Portfolio Eficiente", key="inpulse")
        st.subheader("Se despliegan Herramientas/Modelos estadisticos, opteniendo métricas optimas para la toma de decisiones")
    with right:
               #"""### image from local file"""
        file_ = open("img/report.png", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(
          f'<img src="data:img/gif;base64,{data_url}" alt="imagen" width="120" height="120">',
          unsafe_allow_html=True
        )
st.markdown("---")

st.header("# Detalle de contenido de las páginas ")
st.markdown("---")
### Define Menu--------------
sub_menus = {"Modelo Montecarlo":["Fronteria Eficiencia-Modelo Markowitz","Ratio de Sharpe"],
             "Modelo Clásico":["Frontera Eficiencia-Modelo Markpowitz ", "Diversificación/Ratio Sharpe","Optimización HRP"],
             "Ponderador":["Matriz Correlación/Portfolio ", "Ponderador Riesgo/Rendimiento"]
            }
# Optinally you can supply google icons
sub_menu_icons = {
                  "Modelo Montecarlo": ["leaderboard", "multiline_chart"], 
                  "Modelo Clásico": ["leaderboard", "multiline_chart","trending_up"], 
                  "Ponderador": ["query_stats","candlestick_chart"]
                     
                }

list_of_montecarlo_imgs = ["https://img.freepik.com/vector-gratis/fondo-negocio-global-grafico-cotizaciones-tono-azul_53876-119546.jpg?t=st=1738434263~exp=1738437863~hmac=0d6275a3a8c7c8e68ccdd017dea286ea4f8d186745da077b538e3d15df07a2dd&w=1060",
                        "https://img.freepik.com/vector-gratis/grafico-diagrama-inversion-financiera-mercado-valores-flecha-arriba-sobre-fondo-azul_56104-1814.jpg?t=st=1738434076~exp=1738437676~hmac=1dd05eb5c258da422bb0f95c87e4d9c749a7ce016f36b1d8fbe4cdcfaba0d64c&w=1380"                        
                      ]

list_of_clasico_imgs = ["https://img.freepik.com/vector-gratis/fondo-compraventa-divisas_52683-41604.jpg?t=st=1738434772~exp=1738438372~hmac=fd4c5d3cad3477968157130fa8918b3707837098e9b5d9a435c20dc1c02e3302&w=1060",
                      "https://img.freepik.com/vector-gratis/concepto-mercado-valores-diseno-plano-dibujado-mano_23-2149154265.jpg?t=st=1738434921~exp=1738438521~hmac=72eb0cbd2b1a2ccc9fd19aa5928c1cb68b40cfc65775683ca9c0a67f44d832cd&w=1060",
                      "https://img.freepik.com/vector-gratis/fondo-grafico-mercado-finanzas-obtener-ganancias-digitales_1017-44828.jpg?t=st=1738435075~exp=1738438675~hmac=ae13aa1eb946b0329e6b4625d6486af6f0f28b8174e245868532aeb9dc826373&w=1060",
                      "https://img.freepik.com/vector-gratis/concepto-mercado-valores-degradado_23-2149215737.jpg?t=st=1738434722~exp=1738438322~hmac=9ddf9f87fb42aeb2733013afd955b0afb66c25f803255619f2e4ac6208c2fb52&w=1060"                        
                    ]

list_of_ponderador_imgs = ["https://img.freepik.com/vector-gratis/concepto-mercado-valores-degradado_23-2149215737.jpg?t=st=1738434722~exp=1738438322~hmac=9ddf9f87fb42aeb2733013afd955b0afb66c25f803255619f2e4ac6208c2fb52&w=1060",
                           "https://img.freepik.com/vector-gratis/fondo-particulas-tecnologia-realista-abstracta_23-2148431524.jpg?t=st=1739929874~exp=1739933474~hmac=635b6d0d79ef432fb71d282a915a7cc6cab3968c27eb3cba412ed3cb3156fa99&w=1380",
                           "https://img.freepik.com/vector-gratis/grafico-diagrama-inversion-financiera-mercado-valores-flecha-arriba-sobre-fondo-azul_56104-1814.jpg?t=st=1739929775~exp=1739933375~hmac=618d5e13b2ba11bde924cd511d9b801589937e67b9d846229f515a713c0641fc&w=900",                        
                            "https://img.freepik.com/vector-gratis/concepto-mercado-valores-degradado_23-2149215737.jpg?t=st=1738434722~exp=1738438322~hmac=9ddf9f87fb42aeb2733013afd955b0afb66c25f803255619f2e4ac6208c2fb52&w=1060"
                    ]


# Assign images to corresponding column
sub_menu_imgs = {"Modelo Montecarlo":list_of_montecarlo_imgs,
                 "Modelo Clásico":list_of_clasico_imgs,
                 "Ponderador":list_of_ponderador_imgs                   
                }

selected_menu = streamlit_multi_menu(menu_titles=list(sub_menus.keys()),
                            sub_menus=sub_menus,
                            sub_menu_imgs=sub_menu_imgs,
                            sub_menu_icons = sub_menu_icons,                                               
                            menu_titles_font_size = 25,
                            sub_menu_color = "#690af2",
                            sub_menu_font_size = 15,
                            sub_menu_button_gap = 10,
                            sub_menu_font_color =  "#e8f20a ",
                            sub_menu_border_radius = 8,
                            sub_menu_text_align = 'center',
                            use_container_width=True)


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
      
