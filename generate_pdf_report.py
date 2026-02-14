
import os
import json
import jinja2
import pandas as pd
from datetime import datetime

def load_excel_data(file_path):
    """Loads an excel or csv file and returns a list of dictionaries (rows)."""
    if not file_path or not os.path.exists(file_path):
        return None
    try:
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
            return {
                "headers": df.columns.tolist(),
                "rows": df.values.tolist()
            }
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            return {
                "headers": df.columns.tolist(),
                "rows": df.values.tolist()
            }
    except Exception as e:
        print(f"Error loading excel/csv: {e}")
        return None
    return None

def generate_pdf_report(data_file, output_pdf):
    # 1. Load Data
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    if "date" not in data:
        data["date"] = datetime.now().strftime("%Y-%m-%d")

    # Load Excel Data if provided
    if "excel_files" in data:
        data["excel_data"] = {}
        for key, path in data["excel_files"].items():
            loaded = load_excel_data(path)
            if loaded:
                data["excel_data"][key] = loaded

    # 2. Load CSS from separate file
    css_content = ""
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    # 3. Prepare HTML Template
    template_str = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>{{ project_name }} - Portfolio</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;300;400;700&family=Noto+Sans+KR:wght@100;300;400;700&display=swap" rel="stylesheet">
        <style>
            {{ css_content }}
        </style>
    </head>
    <body>

        <!-- Page 1: Cover -->
        <div class="page">
            <div class="cover-layout">
                <div class="cover-info">
                    <span class="label-small">Architectural Monograph</span>
                    <h1>{{ project_name }}</h1>
                    <p style="font-size: 14pt; margin-top: 5mm; font-weight: 300;">{{ subtitle }}</p>
                    
                    <div style="margin-top: 30mm; border-top: 1px solid #000; padding-top: 10mm; width: 80mm;">
                        <p style="font-size: 8pt; letter-spacing: 2px;">STRATEGIC PLANNING & ANALYSIS</p>
                        <p style="font-size: 8pt; letter-spacing: 2px;">{{ date }}</p>
                    </div>
                </div>
                <div class="cover-visual">
                    {% if masterplan_image %}
                    <img src="{{ masterplan_image }}" alt="Cover Image">
                    {% endif %}
                </div>
            </div>
            <div class="project-meta">UNMA-REDEVELOPMENT // ARCHIVE 2026</div>
            <div class="page-num">01</div>
        </div>

        <div class="page-break"></div>

        <!-- Page 2: Analysis & Context -->
        <div class="page">
            <div class="split-layout">
                <div class="sidebar">
                    <span class="label-small">01 // Context</span>
                    <h2>Project<br>Brief</h2>
                    
                    <table class="premium-table">
                        <tr><td>Location</td><td class="highlight">{{ overview.location }}</td></tr>
                        <tr><td>Site Area</td><td class="highlight">{{ architectural_outline['대지면적'] }}</td></tr>
                        <tr><td>GFA</td><td class="highlight">{{ architectural_outline['연면적'] }}</td></tr>
                        <tr><td>BCR / FAR</td><td class="highlight">{{ architectural_outline['건폐율'] }} / {{ architectural_outline['용적률'] }}</td></tr>
                        <tr><td>Units</td><td class="highlight">{{ architectural_outline['세대수'] }}</td></tr>
                    </table>

                    <div style="margin-top: 15mm;">
                        <span class="label-small">Key Approaches</span>
                        <div class="strategy-list">
                            {% for strategy in strategies %}
                            <div class="strategy-item">
                                <span class="strategy-num">0{{ loop.index }}</span>
                                <p style="font-size: 9pt; color: #333;">{{ strategy }}</p>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
                <div class="main-view">
                    <div class="image-container" style="height: 150mm;">
                        {% if layout_image %}
                        <img src="{{ layout_image }}" alt="Layout Plan">
                        {% endif %}
                    </div>
                    {% if layout_description %}
                    <div class="description-box">
                        <span class="title">SITE LAYOUT & INTEGRATION</span>
                        <p class="text">{{ layout_description }}</p>
                    </div>
                    {% endif %}
                </div>
            </div>
            <div class="page-num">02</div>
        </div>

        <div class="page-break"></div>

        <!-- Page 3: Technical Drawings -->
        <div class="page">
            <div class="split-layout" style="grid-template-columns: 2.5fr 1fr;">
                <div class="main-view">
                    <div class="image-container" style="height: 80mm; margin-bottom: 5mm;">
                        {% if section_image %}
                        <img src="{{ section_image }}" alt="Section">
                        {% endif %}
                    </div>
                    {% if section_description %}
                    <div class="description-box" style="margin-bottom: 5mm;">
                        <span class="title">TOPOGRAPHICAL SECTION AA'</span>
                        <p class="text">{{ section_description }}</p>
                    </div>
                    {% endif %}

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10mm; flex-grow: 1;">
                        <div class="gallery-item">
                            <div class="image-container" style="height: 50mm;">
                                {% if shoring_image %}<img src="{{ shoring_image }}">{% endif %}
                            </div>
                            <div class="description-box">
                                <span class="title">SHORING SYSTEM</span>
                                <p class="text">{{ shoring_description or 'Excavation and lateral support plan.' }}</p>
                            </div>
                        </div>
                        <div class="gallery-item">
                            <div class="image-container" style="height: 50mm;">
                                {% if parking_image %}<img src="{{ parking_image }}">{% endif %}
                            </div>
                            <div class="description-box">
                                <span class="title">PARKING LEVEL B1</span>
                                <p class="text">{{ parking_description or 'Subterranean parking and circulation.' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="sidebar" style="border-right: none; border-left: 1px solid var(--border-color); padding-left: 10mm; padding-right: 0;">
                    <span class="label-small">02 // Engineering</span>
                    <h2>Technical<br>Analysis</h2>
                    <p style="margin-bottom: 10mm;">{{ technical_brief or concept_text }}</p>
                    
                    <div style="background: #000; color: #fff; padding: 8mm; margin-top: 10mm;">
                        <span class="label-small" style="color: #666;">Proposed BCR</span>
                        <div style="font-size: 28pt; font-weight: 200;">{{ architectural_outline['건폐율'] }}</div>
                    </div>
                </div>
            </div>
            <div class="page-num">03</div>
        </div>

        <div class="page-break"></div>

        <!-- Page 4: Interior & Material Schedule (Excel Data) -->
        <div class="page">
            <span class="label-small">03 // Specification</span>
            <h2>Material & Finish<br>Schedules</h2>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15mm; flex-grow: 1;">
                {% if excel_data and excel_data.interior %}
                <div class="excel-table-section">
                    <span class="label-small">Interior Finish Schedule</span>
                    <div style="overflow-y: auto; max-height: 140mm;">
                        <table class="excel-data-table">
                            <thead>
                                <tr>
                                    {% for header in excel_data.interior.headers %}
                                    <th>{{ header }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in excel_data.interior.rows %}
                                <tr>
                                    {% for cell in row %}
                                    <td>{{ cell }}</td>
                                    {% endfor %}
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
                {% endif %}

                <div class="main-view">
                    <div class="image-container" style="height: 80mm;">
                        {% if interior_images %}
                        <img src="{{ interior_images[0] }}">
                        {% endif %}
                    </div>
                    <div class="description-box">
                        <span class="title">INTERIOR ATMOSPHERE</span>
                        <p class="text">High-end finishing materials selected for spatial durability and aesthetic luxury.</p>
                    </div>
                    
                    {% if excel_data and excel_data.landscape %}
                    <div class="excel-table-section" style="margin-top: 5mm;">
                        <span class="label-small">Landscape Quantities</span>
                        <table class="excel-data-table">
                            <thead>
                                <tr>
                                    {% for header in excel_data.landscape.headers[:4] %}
                                    <th>{{ header }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in excel_data.landscape.rows[:10] %}
                                <tr>
                                    {% for cell in row[:4] %}
                                    <td>{{ cell }}</td>
                                    {% endfor %}
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% endif %}
                </div>
            </div>
            <div class="page-num">04</div>
        </div>

        <div class="page-break"></div>

        <!-- Page 5: Residential Units -->
        <div class="page">
            <span class="label-small">04 // Dwelling</span>
            <h2>Unit Plans<br>& Circulation</h2>
            
            <div class="gallery-3col" style="margin-top: 10mm;">
                {% for plan in unit_plans %}
                <div class="gallery-item">
                    <div class="img-wrap"><img src="{{ plan.image }}"></div>
                    <div class="description-box">
                        <span class="title">{{ plan.title }}</span>
                        <p class="text">{{ plan.description or 'Efficient spatial arrangement with maximized natural ventilation.' }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>

            <div class="gallery-3col" style="margin-top: 10mm;">
                {% for plan in core_plans %}
                <div class="gallery-item">
                    <div class="img-wrap"><img src="{{ plan.image }}"></div>
                    <div class="description-box">
                        <span class="title">{{ plan.title }}</span>
                        <p class="text">{{ plan.description or 'Vertical circulation core design.' }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="page-num">05</div>
        </div>

        <div class="page-break"></div>

        <!-- Page 6: Gallery & Visualization -->
        <div class="page">
            <div class="page-header" style="border: none;">
                <span class="label-small">05 // Visualization</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10mm; height: 130mm;">
                <div class="image-container">
                    {% if landscape_image %}
                    <img src="{{ landscape_image }}" style="height: 100%;">
                    {% endif %}
                </div>
                <div style="display: grid; grid-template-rows: 1fr 1fr; gap: 10mm;">
                    <div class="image-container">
                        {% if elevation_images %}
                        <img src="{{ elevation_images[0] }}">
                        {% endif %}
                    </div>
                    <div class="image-container">
                        {% if interior_images and interior_images|length > 1 %}
                        <img src="{{ interior_images[1] }}">
                        {% endif %}
                    </div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10mm; margin-top: 5mm;">
                <div class="description-box">
                    <span class="title">ARCHITECTURAL EXPRESSION</span>
                    <p class="text">The facade design employs high-performance glass and metallic accents, reflecting the urban energy while maintaining residential warmth through integrated landscape elements.</p>
                </div>
                <div class="description-box" style="border-left: 1px solid #eee; padding-left: 5mm; border-top: none; margin-top: 0; padding-top: 0;">
                    <span class="title">CONCLUSION</span>
                    <p class="text" style="font-style: italic;">"A synthesis of urban density and natural serenity."</p>
                </div>
            </div>
            <div class="page-num">06</div>
        </div>

    </body>
    </html>
    """

    # 4. Render HTML
    template = jinja2.Template(template_str)
    html_content = template.render(css_content=css_content, **data)

    temp_html = "report_portfolio_v2.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 5. Convert to PDF
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            abs_path = "file://" + os.path.abspath(temp_html)
            page.goto(abs_path)
            page.wait_for_timeout(3000)
            
            page.pdf(
                path=output_pdf, 
                format="A4", 
                landscape=True, 
                print_background=True,
                margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"}
            )
            browser.close()
        print(f"Successfully generated Premium Portfolio PDF: {output_pdf}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python generate_pdf_report.py <data_json> <output_pdf>")
    else:
        generate_pdf_report(sys.argv[1], sys.argv[2])
