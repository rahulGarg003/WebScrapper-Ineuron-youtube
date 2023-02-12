from fpdf import FPDF
import requests

class CoursePDF():
    class _PDF(FPDF):
        def __init__(self):
            super().__init__()
        def header(self):
            self.set_font('Arial', '', 12)
            # self.cell(0, 8, , 0, 1, 'C')
            # url = r'https://ineuron.ai/images/ineuron-logo.png'
            # img = open('logo.png', 'wb')
            # img.write(requests.get(url).content)
            self.image('logo.png', w=40, h=20, type='PNG',x=210/2-20)
            self.cell(w=0,border=True)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', '', 9)
            self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')

    def __init__(self):
        pass

    def generateCoursePdf(self,data: dict):
        # cell height
        ch = 6
        pdf = self._PDF()
        pdf.add_page()
        pdf.ln(4)
        pdf.set_font('Arial', 'BU', 16)
        pdf.multi_cell(w=0, h=5, txt=data['title'], align='C')
        pdf.ln(4)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(w=0, h=5, txt=data['details']['description'].encode('latin-1', 'replace').decode('latin-1'))
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=210/3, h=ch, txt=f"Mode: {data['details']['mode']}", ln=0)
        pdf.cell(w=210/3, h=ch, txt=f"Language: {data['meta']['overview']['language']}", ln=0)
        pdf.cell(w=210/3, h=ch, txt=f"Duration: {data['meta']['duration']}", ln=1)

        y_pos = 65

        pdf.set_y(y_pos)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="What you'll learn:", ln=1)
        pdf.set_font('Arial', '', 9)
        for d in data['meta']['overview']['learn']:
            pdf.cell(w=30, h=ch, txt=f'{" "*4}{d}', ln=1)
        pdf.ln(4)

        pdf.set_xy(210/3, y_pos)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Course Features:", ln=1)
        pdf.set_font('Arial', '', 9)
        for feature in data['meta']['overview']['features']:
            pdf.set_x(210/3)
            pdf.cell(w=30, h=ch, txt=f'{" "*4}{feature}', ln=1)
        pdf.ln(4)

        pdf.set_xy(210*2/3,y_pos)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Requirements:", ln=1)
        pdf.set_font('Arial', '', 9)
        for d in data['meta']['overview']['requirements']:
            pdf.set_x(210*2/3)
            pdf.cell(w=30, h=ch, txt=f'{" "*4}{d}', ln=1)
        pdf.ln(4)

        pdf.set_x(210*2/3)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Pricing:", ln=1)
        pdf.set_font('Arial', '', 9)
        pdf.set_x(210*2/3)
        pdf.cell(w=0, h=ch, txt=f"{' '*4}{data['details']['pricing']['IN']} INR", ln=1)
        pdf.set_x(210*2/3)
        pdf.cell(w=0, h=ch, txt=f"{' '*4}{data['details']['pricing']['US']} USD", ln=1)

        pdf.set_y(y_pos+(15*ch))
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Course Curriculum:", ln=1)
        pdf.set_font('Arial', '', 9)
        for num, d in enumerate(data['meta']['curriculum'].values()):
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=0, h=ch, txt='{}{}. {}'.format(" "*4,num+1, d['title'].encode('latin-1', 'replace').decode('latin-1')), ln=1)
            for item in d['items']:
                pdf.set_font('Arial', '', 9)
                pdf.cell(w=0, h=ch, txt=f"{' '*12}{item['title'].encode('latin-1', 'replace').decode('latin-1')}", ln=1)
        pdf.ln(4)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Instructors:", ln=1)
        # pdf.set_font('Arial', '', 12)
        for num, d in enumerate(data['meta']['instructordetails'].values()):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(w=0, h=ch, txt='{}. {}'.format(num+1, d['name']), ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(w=0, h=5, txt=d['description'].encode('latin-1', 'replace').decode('latin-1'))
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=30, h=ch, txt=f"{' '*8}Email: ", ln=0)
            pdf.cell(w=100, h=ch, txt=d['email'], ln=1)
            for key, value in d['social'].items():
                pdf.cell(w=30, h=ch, txt=f"{' '*8}{key}: ", ln=0)
                pdf.cell(w=100, h=ch, txt=value, ln=1)
        pdf.ln(4)

        # pdf.cell(w=30, h=ch, txt="Date: ", ln=0)
        # pdf.cell(w=30, h=ch, txt="01/01/2022", ln=1)
        # pdf.cell(w=30, h=ch, txt="Author: ", ln=0)
        # pdf.cell(w=30, h=ch, txt="Max Mustermann", ln=1)
        # pdf.ln(ch)
        # pdf.multi_cell(w=0, h=5, txt="lorem.paragraph()")
        # pdf.ln(ch)
        # pdf.multi_cell(w=0, h=5, txt="lorem.paragraph()")
        pdf.output(f'{data["title"].replace(" ","-")}.pdf', 'F')

if __name__ == '__main__':
    CoursePDF().generateCoursePdf()