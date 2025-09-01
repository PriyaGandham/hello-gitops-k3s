import pandas as pd
from semantic_kernel.functions import kernel_function


sheet_names = [
    'Text - Unstructured Data',
    'Image to text(Captioning)',
    'Image Generation',
    'Image Q&A',
    'Synthetic data generation',
    'Table QnA',
    'Agentic AI',
    'Code',
    'Classical machine learning'
]

description_dimensions = f"""
Choose among one of the following categories to determine the category of the given use case \
and pass that category appropriately in order to get the \
project dimensions details. The categories are:
{"".join(f"- {sname} \n" for sname in sheet_names)}\
"""

description_complexity = f"""
Choose among one of the following categories to determine the category of the given use case \
and pass that category appropriately in order to get the \
project complexity classification details. The categories are:
{"".join(f"- {sname} \n" for sname in sheet_names)}\
"""

class CriteriaPlugin:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = pd.ExcelFile(file_path)

    @kernel_function(
        name = "get_project_dimensions",
        description = description_dimensions
    )
    def determine_dimentions(self, category : str):
        category = category.strip()
        df = pd.read_excel(self.file, category, header = [0, 1])
        csv_string = ', '.join(df.iloc[:, 0].astype(str))
        print(csv_string)
        return f"The key parameters are:\n{csv_string}\nYou have to ."

    @kernel_function(
        name="get_complexity_details",
        description = description_complexity
    )
    def determine_complexity(self, category : str):
        category = category.strip()
        df = pd.read_excel(self.file, category, header = [0, 1])
        df.columns = df.columns.map('_'.join)
        print(df.to_markdown())
        return (
            f"The Complexity criterias are listed below :\n{df.to_markdown()}\n." 
            "You have to choose a singlular most appropriate complexity."
        )
    

