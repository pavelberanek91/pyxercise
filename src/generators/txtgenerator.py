from src.generators.textgenerator import TextGenerator
import os
import codecs

class TxtGenerator(TextGenerator):
    '''
        vygeneruje zadani a reseni testu do souboru typu .txt
    '''


    def generate_file(self, type):
        '''
        
        '''

        # choose folder for test (or solution of test)
        folder = self._solution_folder if type == 'solution' else self._test_folder

        #creates folder for student's test (solution) if folder doesn't exists
        if not os.path.exists(folder):
            os.mkdir(folder)

        #creates file for student's test (solution) in test (solution) folder
        file_extension = '_reseni.txt' if type == 'solution' else '.txt'
        file_name = f'{self._exercise_data["student"]}{file_extension}'
        file_path = os.path.join(os.getcwd(), folder, file_name)
        file = codecs.open(file_path, 'w', encoding='utf-8')

        #reads test name and writes it into test (solution) file
        file.write(f'Test z fyziky: {self._exercise_data["nazev"]}\n\n')
        
        #reads students name and writes it into test (solution) file
        file.write(f'Student: {self._exercise_data["student"]}\n\n')

        #reads exercise introduction text and writes it into test (solution) file
        file.write(f'{self._exercise_data["uvod"]}\n')

        #for each exercise in exercise file write down it's assignment or solution
        exercise_data_key = 'reseni' if type == 'solution' else 'zadani'
        for iassigment, assigment in enumerate(self._exercise_data[exercise_data_key]):
            file.write("Pr. "+str(iassigment+1)+":")
            file.write(assigment+"\n")

        #reades final notes for test and writes it down to test (solution) file
        file.write(f'{self._exercise_data["zaver"]}\n')
        file.close()