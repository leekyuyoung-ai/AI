import time
import requests
from bs4 import BeautifulSoup
from kafka import KafkaProducer

KAFKA_BROKER = "kafka:9092"
TOPIC = "web-data"

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

def fetch_data():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    for item in soup.select(".storylink"):
        articles.append(item.text)

    return articles

while True:
    data = fetch_data()
    for article in data:
        producer.send(TOPIC, article.encode('utf-8'))
    print("✅ Data sent to Kafka")
    time.sleep(10)
