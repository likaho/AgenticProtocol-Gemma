docker build -t streamlit-app .
docker run -d --name streamlit-app --network=web -p 8501:8501 streamlit-app