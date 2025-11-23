import os
import base64
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except Exception:
    print('Missing jinja2. Install with: pip install jinja2')
    raise

# optional matplotlib for small embedded chart
has_matplotlib = True
try:
    import matplotlib.pyplot as plt
except Exception:
    has_matplotlib = False

THIS_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = THIS_DIR / 'ui' / 'widgets'
TEMPLATE_NAME = 'report.html'
OUT = THIS_DIR / 'tmp'
OUT.mkdir(exist_ok=True)
OUT_FILE = OUT / 'report_sample.html'

# sample assessment data matching generate_complete_output shape
sample = {
    'report_date': '2025-11-19',
    'Personal': {
        'name': 'Jane Doe',
        'date_of_birth': '1990-01-01',
        'time_of_birth': '06:30',
        'place_of_birth': 'City, Country',
        'phone': '1234567890',
        'email': 'jane@example.com'
    },
    'Element_Percentages': {'Fire': 35, 'Earth': 20, 'Air': 25, 'Water': 20},
    'Modalities_Percentages': {'Cardinal': 50, 'Fixed': 30, 'Mutable': 20},
    'Element_Descriptions': {
        'Fire': {'Title': 'The Fire Element', 'Content': 'Fire content goes here...', 'Status': 'High', 'Percentage': 35},
        'Earth': {'Title': 'The Earth Element', 'Content': 'Earth content goes here...', 'Status': 'Balanced', 'Percentage': 20},
        'Air': {'Title': 'The Air Element', 'Content': 'Air content goes here...', 'Status': 'Low', 'Percentage': 25},
        'Water': {'Title': 'The Water Element', 'Content': 'Water content goes here...', 'Status': 'Balanced', 'Percentage': 20},
    },
    'Daily_Routine': {
        'Morning': {'Diet': 'Start with warm lemon water', 'Lifestyle': 'Gentle stretching', 'Wear_Clothing': 'Light layers', 'Exercise': 'Walk 20 minutes'},
        'Midday': {'Diet': 'Balanced lunch', 'Lifestyle': 'Short walk', 'Optional': 'Rest 10 minutes'},
        'Evening': {'Diet': 'Light soup', 'Lifestyle': 'Relaxing bath', 'Exercise': 'Light yoga'},
        'Weekly_Addition': 'One long outdoor walk on the weekend'
    },
    'Modality_Descriptions': {'Cardinal': {'Title': 'Cardinal Energy', 'Content': 'Cardinal content...'}},
    'Summary': 'Top recommendations: increase warmth, moderate exercise, and regular sleep schedule.'
}

# generate a small pie chart as base64 PNG if matplotlib available
element_chart_png = None
if has_matplotlib:
    try:
        labels = list(sample['Element_Percentages'].keys())
        sizes = [sample['Element_Percentages'][k] for k in labels]
        colors = ['#ff8a65', '#ffd54f', '#4fc3f7', '#4db6ac']
        fig, ax = plt.subplots(figsize=(3.2, 2.0), dpi=100)
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct='%1.0f%%', colors=colors, startangle=90)
        ax.axis('equal')
        plt.setp(texts, size=8)
        plt.setp(autotexts, size=8)
        buf = None
        import io
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        element_chart_png = base64.b64encode(buf.read()).decode('ascii')
    except Exception as e:
        print('Matplotlib chart generation failed:', e)
        element_chart_png = None

# Render template
env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template(TEMPLATE_NAME)
rendered = template.render(**sample, element_chart_png=element_chart_png)
with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write(rendered)

print(f'Wrote sample report to: {OUT_FILE}')
print('Preview (first 400 chars):')
print(rendered[:400])
