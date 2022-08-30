from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import string

class ActividadPrestatario:
  def __init__(self):
    self.nombre_actividad = ""
    self.numero_vacantes = ""
    self.nombre_prestatario = ""
    self.nombre_largo_prestatario = ""
    self.nombre_programa = ""
    self.fechaInicioTermino = ""
    self.objetivo_programa = ""
    self.justificacion_programa = ""
    self.domicilio_programa = ""
    self.nombre_representante = ""
    self.medios_contacto_representante = ""
    self.apoyos_programa = ""

base = "https://serviciosocial.ipn.mx"
main_page_url = "/infoServSoc/InfoServSocListaPrsttrPerf.do?cvePerfil=53"

def give_format_text(text):
  text_from_div = text
  text_from_div = text_from_div.strip()
  # text_from_div = text_from_div.replace(" ", "")
  text_from_div = " ".join(text_from_div.split())
  # text_from_div = text_from_div.translate({ord(c): None for c in string.whitespace})
  return text_from_div

def get_pages_urls(page_url):
  pages_links = list()
  
  page = requests.get(page_url)
  soup = BeautifulSoup(page.content, 'html.parser')

  todos_links = soup.find_all('a')

  for link in todos_links:
    if link.text == "Ver":
      link_attr = link.get('href')
      pages_links.append(link_attr)
      
  return pages_links
  
def get_page_values_arr(page_url):
  page = requests.get(page_url)
  soup = BeautifulSoup(page.content, 'html.parser')
  
  tabla_contenedor = soup.find_all('div', class_='tabla')
  
  if not(len(tabla_contenedor) > 0):
    return []
  
  contenido = tabla_contenedor[1]
  numero_separador_contenido = 14
  
  contenido_divs = contenido.find_all("div")
  
  contador_divs = 1
  
  actividades_arr = list()
  class_variable = ActividadPrestatario()
  for div in contenido_divs:
    
    if(contador_divs == 1):
      class_variable = ActividadPrestatario()
      
      class_variable.nombre_actividad = give_format_text(div.text)
      
    if(contador_divs == 2):
      class_variable.numero_vacantes = give_format_text(div.text)
      
    if(contador_divs == 3):
      class_variable.nombre_prestatario = give_format_text(div.text)
      
    if(contador_divs == 4):
      class_variable.nombre_largo_prestatario = give_format_text(div.text)
    
    if(contador_divs == 5):
      class_variable.nombre_programa = give_format_text(div.text)
      
    if(contador_divs == 6):
      class_variable.fechaInicioTermino = give_format_text(div.text)
      
    if(contador_divs == 7):
      class_variable.objetivo_programa = give_format_text(div.text)
    
    if(contador_divs == 8):
      class_variable.justificacion_programa = give_format_text(div.text)
    
    if(contador_divs == 9):
      class_variable.domicilio_programa = give_format_text(div.text)
    
    if(contador_divs == 10):
      class_variable.nombre_representante = give_format_text(div.text)
    
    if(contador_divs == 11):
      class_variable.medios_contacto_representante = give_format_text(div.text)
    
    if(contador_divs == 12):
      class_variable.apoyos_programa = give_format_text(div.text)
      
      actividades_arr.append(class_variable)
    
    # Resetear datos
    contador_divs = contador_divs + 1
    
    if contador_divs > 14:
      contador_divs = 1
  
  return actividades_arr

def get_all_pages_values_arr(pages_urls):
  actividades_arr = list()
  
  print("NUMERO PAGINAS: ", len(pages_urls))

  contador_pagina_scrap = 1
  for page_link in pages_urls:
    print("### PAGINA ", contador_pagina_scrap)
    actividades_page_arr = get_page_values_arr(base + page_link)
    actividades_arr.extend(actividades_page_arr)
    
    contador_pagina_scrap = contador_pagina_scrap + 1;    
    
  return actividades_arr;

pages_urls = get_pages_urls(base + main_page_url)
activities_arr = get_all_pages_values_arr(pages_urls)
print("SE HAN OBTENIDO TODOS LOS DATOS ###")
print("Se convertira de clase a json ###")
activities_json = json.dumps([ob.__dict__ for ob in activities_arr], ensure_ascii=False)
print("Conversion de clase a json finalizada ###")
print("Se guardara json en archivo ###")
with open("pages_data.json", "w") as outfile:
  outfile.write(activities_json)
  
print("SE HA GUARDADO EL JSON ###")