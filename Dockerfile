# Python version
FROM python:3.8.6-buster
# Custom port
EXPOSE 8080
# Work Directory
WORKDIR /app
# Preparing the environment
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Installing app files
COPY music_similarity/* /app/music_similarity/
COPY raw_data/* /app/raw_data/
COPY app.py /app/
# Executing command to run app.py
CMD streamlit run app.py
