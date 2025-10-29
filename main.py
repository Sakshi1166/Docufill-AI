from flask import Flask, render_template, request, redirect
import csv
import os
import pandas as pd

app = Flask(__name__)

# --- FORM PAGE ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        dob = request.form.get('dob', '').strip()
        mobile = request.form.get('mobile', '').strip()
        address = request.form.get('address', '').strip()
        father_name = request.form.get('father_name', '').strip()
        aadhaar = request.form.get('aadhaar', '').strip()

        # Create data folder if it doesn’t exist
        os.makedirs('data', exist_ok=True)
        file_path = os.path.join('data', 'data.csv')

        # Save to CSV
        file_exists = os.path.isfile(file_path)
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Date of Birth', 'Mobile', 'Address', 'Father Name', 'Aadhaar'])
            writer.writerow([name, dob, mobile, address, father_name, aadhaar])

        return redirect('/success')

    return render_template('form.html')

# --- SUCCESS PAGE ---
@app.route('/success')
def success():
    return """
    <h2 style='text-align:center; color:green;'>✅ Form submitted successfully!</h2>
    <p style='text-align:center;'><a href='/'>Go Back</a> | <a href='/admin'>View Submissions</a></p>
    """

# --- ADMIN PAGE ---
ADMIN_KEY = "12345"
@app.route('/admin')
def admin():
    file_path = os.path.join('data', 'data.csv')
    if not os.path.exists(file_path):
        return "<h3 style='text-align:center; color:red;'>No data found yet!</h3><p style='text-align:center;'><a href='/'>Go Back</a></p>"

    df = pd.read_csv(file_path)
    records = df.to_dict(orient='records')
    headers = df.columns.tolist()
    return render_template('admin.html', headers=headers, records=records)

if __name__ == '__main__':
    app.run(debug=True)