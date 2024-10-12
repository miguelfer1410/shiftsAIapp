import google.generativeai as genai
from flask import Flask, request, jsonify, send_file
import openpyxl
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

genai.configure(api_key='AIzaSyCl4Vbp3g5Xhwnn17kCk4e4MXfxN2T_Qk4')

def call_gemini_api(input_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        input_text,
        generation_config=genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.2,
        )
    )
    
    if response.candidates:
        structured_schedule = response.candidates[0].content.parts[0].text
        return structured_schedule
    
    return ""

def generate_excel_schedule(schedule_data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Work Schedule"

    for row in schedule_data:
        if len(row) >= 6:  
            sheet.append(row)
        else:
            print(f"Linha inválida, ignorando: {row}")  
    
    for col in range(1, 2):
        col_letter = openpyxl.utils.get_column_letter(col)
        sheet.column_dimensions[col_letter].width = 15

    filename = "./work_schedule.xlsx"
    
    workbook.save(filename)
    return filename

@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    description = request.json.get('description')
    if not description:
        return jsonify({"error": "Description not provided"}), 400

    structured_schedule = call_gemini_api(description)
    
    schedule_data = process_schedule_to_excel_data(structured_schedule)

    print("Schedule Data:", schedule_data)
    
    file_path = generate_excel_schedule(schedule_data)
    
    return send_file(file_path, as_attachment=True)

def process_schedule_to_excel_data(schedule_text):
    print(schedule_text)

    rows = []
    header = []  
    
    lines = schedule_text.splitlines()
    
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in ["Exemplo de preenchimento:", "Horário:", "Tabela:", "Opção", "Dias da semana", "Planilha"]):
            if i + 2 < len(lines):
                header_line = lines[i + 2]
                header = [item.strip() for item in header_line.split("|") if item.strip()]  
                rows.append(header)  

            for j in range(i + 3, len(lines)):  
                if j < len(lines) and lines[j].startswith("|"):
                    row = [item.strip() for item in lines[j].split("|") if item.strip()]
                    if len(row) >= 6: 
                        rows.append(row)  
    
    return rows


if __name__ == '__main__':
    app.run(debug=True)
