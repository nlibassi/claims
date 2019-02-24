# submission/render.py - location may change later

# BytesIO is used for in-memory binary streams
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
# pisa.pisaDocument accepts streams as parameters

class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        file = open("my.file.pdf", "wb")
        # here response gets 'populated' with the output from pisa
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
        file.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)


        @staticmethod
        def render_to_file(path: str, params: dict):
            template = get_template(path)
            html = template.render(params)
            # why the random number in the file name?
            file_name = "{0}-{1}.pdf".format(params['request'].user.first_name, randint(1, 1000000))
            # absolute path of the directory where the program/file resides: os.path.abspath(os.path.dirname("__file__"))
            file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "store", file_name)
            with open(file_path, 'wb') as pdf:
                pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
            return [file_name, file_path]