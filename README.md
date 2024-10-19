# SmartStay-GuestCare
- SmartStay-GuestCare is a sophisticated and interactive hotel chatbot specifically designed to enhance the guest experience by providing real-time information about a wide range of hotel facilities, accommodations, pricing options, and services. This innovative chatbot leverages advanced natural language processing to engage with guests in a conversational manner, allowing them to easily access essential information at any time.

- Whether guests are inquiring about room availability, seeking details about amenities, or looking for the best pricing packages, SmartStay-GuestCare is equipped to deliver accurate and timely responses. The chatbot not only simplifies the process of gathering information but also assists in making informed decisions, ensuring a seamless experience from the moment guests check-in to their departure.

- SmartStay-GuestCare can cater to diverse guest needs, making it an invaluable tool for both the hotel staff and guests. This commitment to providing exceptional service through technology makes SmartStay-GuestCare an essential component of modern hotel operations.

<img src="static/demo1.png">
<img src="static/demo2.png">

## Steps to Run it
### 1. Cloning the Repository
```bash

git clone https://github.com/MANMEET75/SmartStay-GuestCare.git
```
### 2. Creating the virtual environment using anaconda
```bash
conda create -p venv python=3.11 -y
```

### 3. Activate the virtual environment
```bash
conda activate venv/
```

### 4. Install the Requirements
```bash
pip install -r requirements.txt
```
### 5. Run the following docker command in your command prompt
```bash
docker-compose up
```
### 6. Generate the Embeddings
```bash
python ingest.py
```
### 7. Run the FastAPI application
```bash
uvicorn main:app --reload --port 8080
``` 
## Steps to Change the database name
```bash
docker-compose down
```
### Change the Database name from docker-compose.yml file
```bash
docker-compose up
```


Enjoy Coding!
