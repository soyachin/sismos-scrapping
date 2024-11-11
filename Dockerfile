FROM public.ecr.aws/lambda/python:3.12

RUN pip install --upgrade pip && \
    pip install playwright && \
    playwright install --with-deps && \
    pip install requests beautifulsoup4

COPY sismos.py ${LAMBDA_TASK_ROOT}

CMD ["sismos.lambda_handler"]