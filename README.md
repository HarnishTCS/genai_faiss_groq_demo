# genai_faiss_groq_demo

1. genai_faiss_groq_demo\backend> pip install -r .\requirements.txt
2. \genai_faiss_groq_demo\backend> $env:GROQ_API_KEY="<YOUR KEY>"

   Now add some text data to mongoDB by executing insert_data.py file
   
4. \genai_faiss_groq_demo\backend> uvicorn main:app --reload
5. \genai_faiss_groq_demo\frontend> start .\index.html
