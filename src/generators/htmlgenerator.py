from src.generators.textgenerator import TextGenerator
import os
import codecs

class HtmlGenerator(TextGenerator):
    '''
        vygeneruje zadani a reseni testu do souboru typu .html
    '''


    def generate_file(self, type):
        '''
        
        '''

        # choose folder for test (or solution of test)
        folder = self._solution_folder if type == 'solution' else self._test_folder

        #creates folder for student's test (solution) if folder doesn't exists
        if not os.path.exists(folder):
            os.mkdir(folder)

        #start of html content
        head_start = '<!DOCTYPE html>\n<html>\n<head>\n'
        
        #if style file is selected then generate css link to html content
        if self._style_file:
            css_link = f'<link rel="stylesheet" href="{self._style_file}">\n'
        else:
            css_link = ''
        
        #metadata of html document
        title = '<title>Fyzika Test</title>\n'
        meta_charset = '<meta charset="utf-8">\n'
        body_start = '</head>\n<body>\n'
        
        #fragment of html content to end html document
        footer = '</body>\n</html>'

        #reads test name and writes it into test (solution) file content
        header = f'<h1>Test z fyziky: {self._exercise_data["nazev"]}</h1>'
        
        #reads students name and writes it into test (solution) file content
        student = f'<h2>Student: {self._exercise_data["student"]}</h2>\n'

        #reads exercise introduction text and writes it into test (solution) file content
        introduction = '<p id="uvod">'+ self._exercise_data["uvod"] +'</p>'
        
        #reads final notes for test and writes it down to test (solution) file content
        end_note = '<hr>\n<p id="zaver">'+ self._exercise_data["zaver"] +'</p>'
        
        #creates html document content from html fragments
        html_content = head_start + css_link + title + meta_charset
        html_content += body_start + header + student + introduction
        
        #for each exercise in exercise file write down it's assignment or solution
        exercise_data_key = 'reseni' if type == 'solution' else 'zadani'
        for iassigment, assigment in enumerate(self._exercise_data[exercise_data_key]):
            html_content += "<hr>"
            html_content += "<h3>Příklad: "+str(iassigment+1)+"</h3>\n"
            html_content += "<p>"+assigment.replace("\n","<br>")+"</p>\n"
            
        #end html content with final notes and footer section
        html_content += end_note + footer
        
        #creates file for student's test (solution) in test (solution) folder
        file_extension = '_reseni.html' if type == 'solution' else '.html'
        file_name = f'{self._exercise_data["student"]}{file_extension}'
        file_path = os.path.join(os.getcwd(), folder, file_name)
        file = codecs.open(file_path, 'w', encoding='utf-8')

        #writes html content to html file
        file.write(html_content)
        file.close()