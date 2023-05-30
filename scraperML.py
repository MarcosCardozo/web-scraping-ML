import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extraerProductos(p_productos):
    l_productos = []
    fecha_actual = datetime.now()

    for producto in productos:
        nombre_producto = producto.find('h2', class_='ui-search-item__title shops__item-title').get_text()
        precio = producto.find('span', class_='price-tag-fraction').get_text()

        # Uso try-except porque algunos productos no tienen calificacion ni descuento
        try: 
            calificacion_elem = producto.find('span', class_='andes-visually-hidden').get_text()
            calificacion = calificacion_elem.split(' ')[1]
            n_opiniones = calificacion_elem.split(' ')[4]
        except:
            calificacion = None
            n_opiniones = None
        
        try:
            porcentaje_descuento = producto.find('span', attrs={'class':'ui-search-price__discount shops__price-discount'}).get_text().replace('% OFF', '')
        except:
            porcentaje_descuento = None

        l_productos.append([nombre_producto, calificacion, n_opiniones, precio, porcentaje_descuento, fecha_actual.strftime('%d-%m-%Y')])
    
    return pd.DataFrame(l_productos, columns=['nombre_producto', 'calificacion(0-5)', 'n_opiniones', 'precio_original', 'porcentaje_descuento', 'fecha_scrp'])

PRODUCTO = input("Que Producto le gustaria extraer de ML? ")
url = input("Pegue la URL de la pagina de mercado libre del producto de interes: ")
#url = "https://listado.mercadolibre.com.ar/celulares-telefonos/celulares-smartphones/celulares_NoIndex_True#D[A:celulares,on]"

PAGINAS = int(input("\nAhora ingrese el número de paginas que desea scrapear: "))

df_productos=pd.DataFrame()


try: 
    for i in range(PAGINAS):

        res = requests.get(url)

        soup = BeautifulSoup(res.content, 'html.parser')

        productos = soup.find_all('div', attrs={'class':'ui-search-result__content-wrapper shops__result-content-wrapper'})
        df_productos =  pd.concat([df_productos, extraerProductos(productos)], axis=0)
        
        url = soup.find('a', class_='andes-pagination__link shops__pagination-link ui-search-link').get('href')

    df_productos.to_csv(PRODUCTO+'.csv', index=False)

    print("Se han cargado todos los productos correctamente...")
except:
    print("No se pudieron cargar los productos...")