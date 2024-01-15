from bs4 import BeautifulSoup
import requests
import json
import string
from entities import Actividad
import pandas as pd
import sqlite3

DOMAIN_NAME = "https://serviciosocial.ipn.mx"

def clean_text(text):
  text_from_div = text
  text_from_div = text_from_div.strip()
  text_from_div = " ".join(text_from_div.split())
  # text_from_div = text_from_div.translate({ord(c): None for c in string.whitespace})
  return text_from_div

# GET URLS
def get_urls_of_detail_pages(page_url):
  pages_links = list()
  
  page = requests.get(page_url)
  soup = BeautifulSoup(page.content, 'html.parser')

  todos_links = soup.find_all('a')

  for link in todos_links:
    if link.text == "Ver":
      link_attr = link.get('href')
      pages_links.append(link_attr)
      
  return pages_links
  
# GET ACTIVITIES FROM A PAGE
def get_activities_from_detail_page(page_url):
  page = requests.get(page_url)
  soup = BeautifulSoup(page.content, 'html.parser')
  
  divs_con_clase_tabla = soup.find_all('div', class_='tabla')
  
  if not(len(divs_con_clase_tabla) > 0):
    return []
  
  tabla_con_actividades = divs_con_clase_tabla[1]
  numero_filas_por_actividad = 14
  
  filas_de_actividades = tabla_con_actividades.find_all("div")
  numero_filas_de_tabla = len(filas_de_actividades)
  cantidad_actividades = numero_filas_de_tabla // numero_filas_por_actividad
  
  lista_actividades = list()
  # Recurre tabla segun numero de actividades
  for actividad_actual in range(cantidad_actividades):
    sumar_para_fila_actual = actividad_actual * 14
    clase_actividad = Actividad()
    
    for fila_actividad_actual in range(14):
      if(fila_actividad_actual == 1 + sumar_para_fila_actual):
        clase_actividad.nombre_actividad = clean_text(filas_de_actividades[fila_actividad_actual].text)
        
      if(fila_actividad_actual == 2 + sumar_para_fila_actual):
        clase_actividad.numero_vacantes = clean_text(filas_de_actividades[fila_actividad_actual].text)
        
      if(fila_actividad_actual == 3 + sumar_para_fila_actual):
        clase_actividad.nombre_prestatario = clean_text(filas_de_actividades[fila_actividad_actual].text)
        
      if(fila_actividad_actual == 4 + sumar_para_fila_actual):
        clase_actividad.nombre_largo_prestatario = clean_text(filas_de_actividades[fila_actividad_actual].text)
      
      if(fila_actividad_actual == 5 + sumar_para_fila_actual):
        clase_actividad.nombre_programa = clean_text(filas_de_actividades[fila_actividad_actual].text)
        
      if(fila_actividad_actual == 6 + sumar_para_fila_actual):
        clase_actividad.fechaInicioTermino = clean_text(filas_de_actividades[fila_actividad_actual].text)
        
      if(fila_actividad_actual == 7 + sumar_para_fila_actual):
        clase_actividad.objetivo_programa = clean_text(filas_de_actividades[fila_actividad_actual].text)
      
      if(fila_actividad_actual == 8 + sumar_para_fila_actual):
        clase_actividad.justificacion_programa = clean_text(filas_de_actividades[fila_actividad_actual].text)
      
      if(fila_actividad_actual == 9 + sumar_para_fila_actual):
        clase_actividad.domicilio_programa = clean_text(filas_de_actividades[fila_actividad_actual].text)
      
      if(fila_actividad_actual == 10 + sumar_para_fila_actual):
        clase_actividad.nombre_representante = clean_text(filas_de_actividades[fila_actividad_actual].text)
      
      if(fila_actividad_actual == 11 + sumar_para_fila_actual):
        clase_actividad.medios_contacto_representante = clean_text(filas_de_actividades[fila_actividad_actual].text)
      
      if(fila_actividad_actual == 12 + sumar_para_fila_actual):
        clase_actividad.apoyos_programa = clean_text(filas_de_actividades[fila_actividad_actual].text)
        break
      
    lista_actividades.append(clase_actividad)
  
  return lista_actividades

# GET ALL ACTIVITIES FROM ALL PAGES
def get_all_activities(urls):
  activities = list()
  
  print("### GET ACTIVITIES FROM DETAIL PAGES")
  page_counter = 1
  for url in urls:
    print("### PAGE ", page_counter)
    page_activities = get_activities_from_detail_page(DOMAIN_NAME + url)
    activities.extend(page_activities)
    print("### COMPLETED")
    page_counter = page_counter + 1
  
  return activities



def main2():
  CECYT_13_INFORMATICA_PAGE = "/infoServSoc/InfoServSocListaPrsttrPerf.do?cvePerfil=53"
  pages_urls = get_urls_of_detail_pages(DOMAIN_NAME + CECYT_13_INFORMATICA_PAGE)
  activities = get_all_activities(pages_urls)
  df = pd.DataFrame().from_records(activities)
  print(df)
  
  db_connection = sqlite3.connect('dbActividadesSiss.db')
  c = db_connection.cursor()
  
  df.to_sql('dbActividadesSiss', db_connection, if_exists='append')
  
  
  
def main():
  print("")
  f = open('pages_data.json')
  data = json.load(f)
  df = pd.DataFrame().from_records(data)
  f.close()
  
  db_connection = sqlite3.connect('dbActividadesSiss.db')
  c = db_connection.cursor()
  
  df.to_sql('dbActividadesSiss', db_connection, if_exists='append')
  db_connection.close()

if __name__ == "__main__":
  main()