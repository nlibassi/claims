# submission/render.py - location may change later

# BytesIO is used for in-memory binary streams
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import os
# pisa.pisaDocument accepts streams as parameters

class Render:

    @staticmethod
    def render(path: str, params: dict):
        """ renders pdf to display for user """
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        # is this file name a placeholder?
        #file = open('my.file.pdf', 'wb')
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        #file.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        patient_name = params['patient_name'].replace(' ', '_')
        date = params['today'].strftime("%Y%m%d_%H-%M-%S")
        file_name = 'Claim_Report_{0}_{1}.pdf'.format(patient_name, date)
        file_path = os.path.join(os.path.abspath(os.path.dirname('__file__')), 'store', file_name)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode('UTF-8')), pdf)
        #return [file_name, file_path]
        return file_path
