# from flask import Flask, request, render_template, send_file, redirect
# import os
# import pandas as pd

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DATA_FILE = os.path.join(UPLOAD_FOLDER, 'restaurant_data.csv')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     if file:
#         file.save(DATA_FILE)
#     return redirect('/')

# @app.route('/display')
# def display():
#     if os.path.exists(DATA_FILE):
#         df = pd.read_csv(DATA_FILE)
#         return df.to_html()
#     return "No file uploaded."

# @app.route('/download', methods=['GET'])
# def download():
#     date = request.args.get('date')
#     restaurant = request.args.get('restaurant')
#     if not os.path.exists(DATA_FILE):
#         return "No data"

#     df = pd.read_csv(DATA_FILE)
#     filtered = df[(df['date'] == date) & (df['restaurant'] == restaurant)]
#     output_file = os.path.join(UPLOAD_FOLDER, 'filtered_data.csv')
#     filtered.to_csv(output_file, index=False)
#     return send_file(output_file, as_attachment=True)

# @app.route('/delete', methods=['POST'])
# def delete():
#     date = request.form['date']
#     restaurant = request.form['restaurant']
#     if not os.path.exists(DATA_FILE):
#         return "No data"

#     df = pd.read_csv(DATA_FILE)
#     df = df[~((df['date'] == date) & (df['restaurant'] == restaurant))]
#     df.to_csv(DATA_FILE, index=False)
#     return f"Deleted data for {restaurant} on {date}"

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, send_file, redirect
import os
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATA_FILE = os.path.join(UPLOAD_FOLDER, 'restaurant_data.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(DATA_FILE)
    return redirect('/')

@app.route('/display')
def display():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        return df.to_html()
    return "No file uploaded."

@app.route('/download', methods=['GET'])
def download():
    date = request.args.get('date')
    restaurant = request.args.get('restaurant')

    if not os.path.exists(DATA_FILE):
        return "No data uploaded yet."

    df = pd.read_csv(DATA_FILE)

    # Normalize columns for case-insensitive match
    df['restaurant'] = df['restaurant'].astype(str).str.lower()
    restaurant = restaurant.strip().lower()

    # Filter by date and restaurant (case-insensitive)
    filtered = df[(df['date'] == date) & (df['restaurant'] == restaurant)]

    if filtered.empty:
        return f"No data found for '{restaurant}' on {date}."

    output_file = os.path.join(UPLOAD_FOLDER, 'filtered_data.csv')
    filtered.to_csv(output_file, index=False)

    return send_file(output_file, as_attachment=True)

@app.route('/delete', methods=['POST'])
def delete():
    date = request.form['date']
    restaurant = request.form['restaurant']
    if not os.path.exists(DATA_FILE):
        return "No data"

    df = pd.read_csv(DATA_FILE)
    df['restaurant'] = df['restaurant'].astype(str).str.lower()
    restaurant = restaurant.strip().lower()

    df = df[~((df['date'] == date) & (df['restaurant'] == restaurant))]
    df.to_csv(DATA_FILE, index=False)

    return f"Deleted data for {restaurant} on {date}"

if __name__ == '__main__':
    app.run(debug=True)
