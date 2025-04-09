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
    df = pd.read_csv('data/data.csv', encoding='utf-8')

    # البحث عن الكلمة باستخدام regex للتأكد أنها كلمة كاملة
    matching_rows = df[df['aya_text_emlaey'].apply(
        lambda x: bool(re.search(rf'\b{re.escape(query)}\b', str(x), flags=re.IGNORECASE))
    )]

    # إحصاء التكرار في القرآن والسورة
    sura_counts = {}  # قاموس لحفظ عدد التكرار في السورة
    total_count = 0  # عدد التكرار في القرآن
    results = []

    for _, row in matching_rows.iterrows():
        sura_name = row['sura_name_ar']
        
        # تحديث عدد التكرار في السورة
        if sura_name not in sura_counts:
            sura_counts[sura_name] = 0
        sura_counts[sura_name] += 1
        total_count += 1
        
        # إضافة النتيجة مع رقم التكرار في السورة
        results.append({
            'رقم': sura_counts[sura_name],  # رقم التكرار في السورة
            'سورة': sura_name,
            'آية': row['aya_text_emlaey']
        })

    return render_template('results.html', query=query, results=results, total_count=total_count)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)