from flask import Flask, render_template, request
import pandas as pd
import re
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']  # الحصول على الكلمة من النموذج

    # تحميل ملف CSV
    df = pd.read_csv('/home/mhmood/Desktop/form.py/alqrain/data/data.csv', encoding='utf-8')

    # البحث عن الكلمة باستخدام regex للتأكد أنها كلمة كاملة
    matching_rows = df[df['aya_text_emlaey'].apply(
        lambda x: bool(re.search(rf'\b{re.escape(query)}\b', str(x), flags=re.IGNORECASE))
    )]

    results = []
    for _, row in matching_rows.iterrows():
        results.append({
            'رقم': row['id'],
            'سورة': row['sura_name_ar'],
            'آية': row['aya_text_emlaey']
        })

    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
