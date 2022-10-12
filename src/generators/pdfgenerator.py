from src.generators.textgenerator import TextGenerator
from src.generators.htmlgenerator import HtmlGenerator
import os
import pdfkit

#TODO: create config file or do it without wkhtmltopdf completly
#PATH_WKHTMLTOPDF = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
PATH_WKHTMLTOPDF = "/usr/local/bin/wkhtmltopdf"

class PdfGenerator(TextGenerator):
    '''
        vygeneruje zadani a reseni testu do souboru typu .pdf
    '''

    def generate_file(self, type):
        '''
        
        '''

        html_generator = HtmlGenerator(
            exercise_data=self._exercise_data,
            test_folder=self._test_folder,
            solution_folder=self._solution_folder,
            style_file=self._style_file
        )
        html_generator.generate_file(type=type)

        # choose folder for test (or solution of test)
        folder = self._solution_folder if type == 'solution' else self._test_folder

        #creates path for source html and target location of generated pdf file
        file_extension_pdf = '_reseni.pdf' if type == 'solution' else '.pdf'
        file_extension_html = '_reseni.html' if type == 'solution' else '.html'
        file_name_pdf = f'{self._exercise_data["student"]}{file_extension_pdf}'
        file_name_html = f'{self._exercise_data["student"]}{file_extension_html}'
        file_path_pdf = os.path.join(os.getcwd(), folder, file_name_pdf)
        file_path_html = os.path.join(os.getcwd(), folder, file_name_html)

        #TODO - is there a way to make pdf without pdfkit? so user doesnt have to install anything?
        config = pdfkit.configuration(wkhtmltopdf = PATH_WKHTMLTOPDF)
        options = {'enable-local-file-access': None}
        pdfkit.from_url(file_path_html, file_path_pdf, configuration=config, options=options)
        pdfkit.from_url(file_path_html, file_path_pdf, configuration=config, options=options)

        if os.path.exists(file_path_html):
            os.remove(file_path_html)