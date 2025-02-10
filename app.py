from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def run_streamlit():
    os.system("streamlit run streamlit.py")
    return "Streamlit app is running... Open http://127.0.0.1:8501"

if __name__ == '__main__':
    app.run(debug=True)