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

    
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table')
    if not table:
        return {
            'statusCode': 404,
            'body': 'No se encontró la tabla en la página web'
        }

    headers = [header.text for header in table.find_all('th')]

    # Extraer las filas de la tabla
    rows = []
    for row in table.find_all('tr')[1:]:  # Omitir el encabezado
        cells = row.find_all('td')
        if len(cells) != len(headers):
            continue  # Skip rows that don't match the header length
        rows.append({headers[i]: cell.text for i, cell in enumerate(cells)})

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

    return {
        'statusCode': 200,
        'body': 'Datos actualizados correctamente'
    }