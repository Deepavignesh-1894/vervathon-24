from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Define the path to your CSV file
CSV_FILE_PATH = r'D:\Vervathon\Economic_Output.csv'  # Update with your file path

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_json = None
    bar_json = None
    funnel_json = None
    line_json = None
    error = None

    if request.method == 'POST':
        year = request.form['year']  # Get the year from the form

        # Read data from the CSV file
        try:
            df = pd.read_csv(CSV_FILE_PATH, encoding='ISO-8859-1')  # Adjust encoding if needed

            # Check if the column exists in the DataFrame
            if year in df.columns:
                # Pie chart
                fig_pie = px.pie(df, names='State', values=year, title=f'Pie Chart for {year}')
                graph_json = pio.to_json(fig_pie)  # Convert to JSON for rendering

                # Bar chart
                fig_bar = px.bar(df, x='State', y=year, title=f'Bar Chart for {year}')
                bar_json = pio.to_json(fig_bar)

                # Funnel chart
                fig_funnel = px.funnel(df, x='State', y=year, title=f'Funnel Chart for {year}')
                funnel_json = pio.to_json(fig_funnel)

                # Line graph (assuming data over time is available)
                fig_line = px.line(df, x='State', y=year, title=f'Line Graph for {year}')
                line_json = pio.to_json(fig_line)
            else:
                error = f"Year '{year}' is not a valid column in the data."
        except Exception as e:
            error = str(e)  # Capture any errors during file reading or processing

    return render_template('index.html', graph_json=graph_json, bar_json=bar_json, funnel_json=funnel_json, line_json=line_json, error=error)

if __name__ == '__main__':
    app.run(debug=True)
