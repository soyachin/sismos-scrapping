import requests
from bs4 import BeautifulSoup
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os
import uuid

def lambda_handler(event, context):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/opt/chrome/chrome"

    driver = webdriver.Chrome(service=ChromeService("/opt/chromedriver"), options=chrome_options)

    url = "https://www.igp.gob.pe/servicios/centro-sismologico-nacional/ultimo-sismo/sismos-reportados"
    driver.get(url)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'id': 'sismosreportados'})
    if not table:
        print("No se encontró la tabla en la página web")
        return {
            'statusCode': 404,
            'body': 'No se encontró la tabla en la página web'
        }

    headers = [header.text.strip() for header in table.find_all('th')]
    print("Encabezados extraídos:", headers)

    # Extraer las filas de la tabla
    rows = []
    for row in table.find('tbody').find_all('tr'):  # Buscar en el cuerpo de la tabla
        cells = row.find_all('td')
        if len(cells) != len(headers):
            print("Fila omitida por longitud inconsistente:", cells)
            continue  # Skip rows that don't match the header length
        rows.append({headers[i]: cell.text.strip() for i, cell in enumerate(cells)})

    # Imprimir los datos extraídos para depuración
    print("Datos extraídos:", rows)

    # Guardar los datos en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Sismos')

    # Eliminar todos los elementos de la tabla antes de agregar los nuevos
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(Key={'id': each['id']})

    # Agregar los nuevos elementos a la tabla
    with table.batch_writer() as batch:
        for row in rows:
            row['id'] = str(uuid.uuid4())
            batch.put_item(Item=row)

    print("Datos guardados en DynamoDB")

    return {
        'statusCode': 200,
        'body': 'Datos actualizados correctamente'
    }