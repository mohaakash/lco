import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_template():
    tpl_dir = os.path.join(os.path.dirname(__file__), '..', 'ui', 'widgets')
    env = Environment(loader=FileSystemLoader(tpl_dir),
                      autoescape=select_autoescape(['html', 'xml']))
    return env.get_template('report.html')


def sample_payload():
    return {
        'Personal': {
            'name': 'Test User',
            'date_of_birth': '1990-01-01',
            'time_of_birth': '12:00',
            'place_of_birth': 'Testville'
        },
        'Element_Percentages': {'Fire': 30, 'Earth': 25, 'Air': 20, 'Water': 25},
        'Modalities_Percentages': {'Cardinal': 40, 'Fixed': 30, 'Mutable': 30},
        'Element_Descriptions': {
            'Fire': {'Title': 'Fiery Nature', 'Content': 'Active, dynamic and warm.', 'Percentage': 30, 'Status': 'Balanced'},
            'Earth': {'Title': 'Grounded', 'Content': 'Stable and practical.', 'Percentage': 25, 'Status': 'Balanced'},
            'Air': {'Title': 'Intellectual', 'Content': 'Curious and communicative.', 'Percentage': 20, 'Status': 'Low'},
            'Water': {'Title': 'Emotional', 'Content': 'Sensitive and intuitive.', 'Percentage': 25, 'Status': 'High'},
        },
        'Modality_Descriptions': {
            'Cardinal': {'Title': 'Initiating', 'Content': 'Starts things', 'Percentage': 40},
            'Fixed': {'Title': 'Sustaining', 'Content': 'Maintains things', 'Percentage': 30},
            'Mutable': {'Title': 'Adapting', 'Content': 'Adapts to change', 'Percentage': 30},
        },
        'Daily_Routine': {'Morning': {'Wake': '6:00 AM', 'Practice': 'Light exercise'}, 'Evening': 'Wind down early'},
        'Summary': 'This is a generated summary.'
    }


def test_report_renders_with_element_percentages():
    tpl = load_template()
    html = tpl.render(**sample_payload())

    # Basic assertions to ensure key sections and values are present
    assert 'Elemental Analysis' in html
    assert 'Element Percentages' in html or 'Element Percentages:' in html
    # Element names
    assert 'Fire' in html
    assert 'Earth' in html
    # Percentages as strings
    assert '30' in html
    assert '25' in html
    # Element content
    assert 'Active, dynamic and warm.' in html
    assert 'Stable and practical.' in html
