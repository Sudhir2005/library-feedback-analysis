# app.py (Flask backend)

from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app = Flask(__name__)

# Function to generate pie charts for each column
def generate_pie_charts(df):
    pie_charts = []
    for column in df.columns:
        # Generate pie chart for each column
        data = df[column].value_counts()
        plt.figure(figsize=(8, 6))
        plt.pie(data, labels=data.index, autopct='%1.1f%%')
        plt.title(f'Pie Chart Analysis - {column}')
        # Convert plot to base64 string
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()  # Close the plot to avoid memory leaks
        pie_charts.append(plot_url)
    return pie_charts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the uploaded Excel file to a temporary location
        excel_path = 'uploaded_excel.xlsx'
        file.save(excel_path)
        # Convert Excel file to CSV format
        df = pd.read_excel(excel_path)
        csv_path = 'uploaded_csv.csv'
        df.to_csv(csv_path, index=False)
        # Generate pie charts for the CSV data
        df_csv = pd.read_csv(csv_path)
        pie_charts = generate_pie_charts(df_csv)
        # Delete temporary files
        os.remove(excel_path)
        os.remove(csv_path)
        # Return result
        return render_template('result.html', pie_charts=pie_charts)

if __name__ == '__main__':
    app.run(debug=True)
