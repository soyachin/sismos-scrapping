FROM public.ecr.aws/lambda/python:3.8

# Instalar las dependencias y Playwright
RUN pip install playwright && \
    playwright install --with-deps \
    requests \
    beautifulsoup4 


# Copia tu código Lambda al contenedor
COPY sismos.py ${LAMBDA_TASK_ROOT}

# Comando de entrada para la Lambda
CMD ["sismos.lambda_handler"]
