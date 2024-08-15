# *Introduction*
<img width="500" alt="Screenshot 2024-08-15 at 5 44 27 PM" src="https://github.com/user-attachments/assets/57baf3de-2513-4bbe-8acd-943af0592239">

SummarAI is an app that allows you to summarize PDFs and ask questions about them. The motivation behind this app was to help students study. When studying for classes,
I found it greatly beneficial to first get an idea of what I'm going to learn. This can be applied to all PDFs. 

This app uses EvaDB, an AI database system that makes it easy to use machine learning models on SQL and vector databases. Here it is used to help summarize content 
from a user's given PDF (EvaDB's in built support for BART is used in this app). SQLite is the default database engine that EvaDB connects to. 

<img src="https://github.com/user-attachments/assets/46fba8bb-8299-48dd-b143-845c1d1c66dc" alt="image" width="350" height="250"/>


# *Step up*

<img src="https://github.com/user-attachments/assets/34ea4cea-26de-4303-adb5-296ec9d5995c" alt="image" width="200" height="200"/>

Ensure python version >= 3.9

Install required libraries: 

pip install --upgrade evadb

pip install groq

Set up API key: 
you can get your API key from groq very easily 

although EvaDB has great built in support for openai I kept running into error code 429 which is why I decided to use groq instead 

entire this commnand in terminal 

export GROQ_API_KEY="your key"

# *Usage*

python summarize.py 

# *Example*
<img width="938" alt="Screenshot 2024-08-15 at 4 37 50 PM" src="https://github.com/user-attachments/assets/2043d416-1cac-43da-af9c-7788d2cf4754">
<img width="942" alt="Screenshot 2024-08-15 at 4 38 14 PM" src="https://github.com/user-attachments/assets/22395c0e-36e5-4e97-acd9-123d383a9456">














