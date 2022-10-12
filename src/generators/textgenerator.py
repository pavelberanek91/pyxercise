from abc import ABC, abstractmethod

class TextGenerator(ABC):


    def __init__(self, exercise_data: dict, test_folder: str, solution_folder: str, 
                    style_file: str) -> None:
        self._exercise_data = exercise_data
        self._test_folder = test_folder
        self._solution_folder = solution_folder
        self._style_file = style_file


    @property 
    def exercise_data(self) -> dict:
        return self._exercise_data


    @exercise_data.setter
    def exercise_data(self, value: dict) -> None:
        self._exercise_data = value


    @property
    def test_folder(self) -> str:
        return self._test_folder


    @test_folder.setter
    def test_folder(self, value: str) -> None:
        self._test_folder = value


    @property 
    def solution_folder(self) -> str:
        return self._solution_folder


    @solution_folder.setter
    def solution_folder(self, value: str) -> None:
        self._solution_folder = value


    @property 
    def style_file(self) -> str:
        return self._style_file


    @style_file.setter
    def style_file(self, value: str) -> None:
        self._style_file = value


    @abstractmethod
    def generate_file(self, type):
        ...