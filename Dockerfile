FROM python:3.8.6-buster
EXPOSE 8501

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY music_similarity/* /app/music_similarity/
COPY raw_data/* /app/raw_data/
COPY app.py /app/
CMD streamlit run app.py
