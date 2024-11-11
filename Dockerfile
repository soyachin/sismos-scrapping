FROM umihico/aws-lambda-selenium-python:latest

# Install Python packages
RUN pip install --upgrade pip && \
    pip install requests beautifulsoup4 boto3

# lambda code copy
COPY sismos.py ${LAMBDA_TASK_ROOT}

CMD ["sismos.lambda_handler"]
