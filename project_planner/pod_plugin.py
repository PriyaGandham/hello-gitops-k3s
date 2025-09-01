from semantic_kernel.functions import kernel_function
import pandas as pd

complexities = [
    'simple',
    'medium',
    'complex'
]

class PODPlugin:
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel_file = pd.ExcelFile(self.file_path)
    
    @kernel_function(
        name = "get_pod_details",
        description = (
            "Choose among the following complexities which is relevant to the"
            "task at hand and pass it accordingly."
            f"{"".join(f"- {c} \n" for c in complexities)}"
        )
    )
    def get_pod_details(self, complexity : str):
        complexity = complexity.strip()
        df = pd.read_excel(self.excel_file, complexity)
        print(df.to_markdown())
        return f"The POD composition is :\n{df.to_markdown()}"
        