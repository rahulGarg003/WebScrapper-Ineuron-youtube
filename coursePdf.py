from fpdf import FPDF
import requests
import os

class CoursePDF():
    class _PDF(FPDF):
        def __init__(self):
            super().__init__()
        def header(self):
            self.set_font('Arial', '', 12)
            if(not os.path.exists('./logo.png')):
                url = r'https://ineuron.ai/images/ineuron-logo.png'
                img = open('logo.png', 'wb')
                img.write(requests.get(url).content)
            self.image('logo.png', w=40, h=20, type='PNG',x=210/2-20)
            self.cell(w=0,border=True)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', '', 9)
            self.cell(w=0,border=True)
            self.cell(0, 8, f'Page {self.page_no()}', 0, 0, 'C')

    def __init__(self):
        pass

    def __formatText(self, txt):
        return str(txt).encode('latin-1', 'replace').decode('latin-1')

    def generateCoursePdf(self,data: dict, savePdf=True):
        # cell height
        ch = 6
        pdf = self._PDF()
        pdf.add_page()
        pdf.ln(4)
        pdf.set_font('Arial', 'BU', 16)
        pdf.multi_cell(w=0, h=5, txt=self.__formatText(data.get('title','')), align='C')
        pdf.ln(4)
        pdf.set_font('Arial', '', 9)
        pdf.multi_cell(w=0, h=5, txt=self.__formatText(data.get('details',{}).get('description','')))
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(w=210/3, h=ch, txt=f"Mode: {self.__formatText(data.get('details','').get('mode'))}", ln=0)
        pdf.cell(w=210/3, h=ch, txt=f"Language: {self.__formatText(data.get('meta',{}).get('overview',{}).get('language',''))}", ln=0)
        pdf.cell(w=210/3, h=ch, txt=f"Duration: {self.__formatText(data.get('meta',{}).get('duration',''))}", ln=1)

        # y_pos = 65

        # pdf.set_y(y_pos)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="What you'll learn:", ln=1)
        pdf.set_font('Arial', '', 9)
        for d in data.get('meta',{}).get('overview',{}).get('learn',[]):
            pdf.cell(w=30, h=ch, txt=f'{" "*4}{self.__formatText(d)}', ln=1)
        pdf.ln(2)

        # pdf.set_xy(210/3, y_pos)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Course Features:", ln=1)
        pdf.set_font('Arial', '', 9)
        for feature in data.get('meta',{}).get('overview',{}).get('features',[]):
            # pdf.set_x(210/3)
            pdf.cell(w=30, h=ch, txt=f'{" "*4}{self.__formatText(feature)}', ln=1)
        pdf.ln(2)

        # pdf.set_xy(210*2/3,y_pos)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Requirements:", ln=1)
        pdf.set_font('Arial', '', 9)
        for d in data.get('meta',{}).get('overview',{}).get('requirements',[]):
            # pdf.set_x(210*2/3)
            pdf.cell(w=30, h=ch, txt=f'{" "*4}{self.__formatText(d)}', ln=1)
        pdf.ln(2)

        # pdf.set_x(210*2/3)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Pricing:", ln=1)
        pdf.set_font('Arial', '', 9)
        # pdf.set_x(210*2/3)
        pdf.cell(w=0, h=ch, txt=f"{' '*4}{self.__formatText(data.get('details',{}).get('pricing',{}).get('IN',''))} INR", ln=1)
        # pdf.set_x(210*2/3)
        pdf.cell(w=0, h=ch, txt=f"{' '*4}{self.__formatText(data.get('details',{}).get('pricing',{}).get('US',''))} USD", ln=1)
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Course Curriculum:", ln=1)
        pdf.set_font('Arial', '', 9)
        for num, d in enumerate(data.get('meta',{}).get('curriculum',{}).values()):
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(w=0, h=ch, txt='{}{}. {}'.format(" "*4,num+1, self.__formatText(d.get('title',''))), ln=1)
            for item in d['items']:
                pdf.set_font('Arial', '', 9)
                pdf.cell(w=0, h=ch, txt=f"{' '*12}{self.__formatText(item.get('title'))}", ln=1)
        pdf.ln(2)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=30, h=ch, txt="Instructors:", ln=1)
        for num, d in enumerate(data.get('meta',{}).get('instructordetails',{}).values()):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(w=0, h=ch, txt='{}. {}'.format(num+1, self.__formatText(d.get('name',''))), ln=1)
            pdf.set_font('Arial', '', 9)
            pdf.multi_cell(w=0, h=5, txt=self.__formatText(d.get('description','')))
            pdf.set_font('Arial', '', 9)
            pdf.cell(w=30, h=ch, txt=f"{' '*8}Email: ", ln=0)
            pdf.cell(w=100, h=ch, txt=self.__formatText(d.get('email','')), ln=1)
            for key, value in d.get('social',{}).items():
                pdf.cell(w=30, h=ch, txt=f"{' '*8}{self.__formatText(key)}: ", ln=0)
                pdf.cell(w=100, h=ch, txt=self.__formatText(value), ln=1)
        # pdf.ln(4)

        if(savePdf):
            if(not os.path.exists('./pdfs')):
                os.mkdir('./pdfs')
            pdf.output(f'./pdfs/{data.get("title","testpdf").replace(" ","-")}.pdf', 'F')
            return f'Pdf has been saved at ./pdfs/{data.get("title","testpdf").replace(" ","-")}.pdf'
        else:
            return pdf.output(f'{data.get("title","testpdf").replace(" ","-")}.pdf', 'S').encode('latin-1')

if __name__ == '__main__':
    CoursePDF().generateCoursePdf()