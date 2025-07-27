import pandas as pd
from tqdm.notebook import tqdm
from openai import OpenAI
from config import METISAI_API_KEY, METISAI_OPENAI_URL

tqdm.pandas()

class Evaluator:

    def __init__(self, csv_path:str, question_c: str, correct_answer_c:str,
                    predicted_answer_c:str, model_name:str):

            self.csv_path = csv_path
            self.question_c = question_c
            self.correct_answer_c = correct_answer_c
            self.predicted_answer_c = predicted_answer_c
            self.model_name = model_name
            
            self.create_judge()
        
    def create_judge(self):
         
        judge = OpenAI(
            api_key=METISAI_API_KEY,
            base_url=METISAI_OPENAI_URL
        )

        self.judge = judge

    def ask_judge(self, question, correct_answer, predicted_answer):

        system_prompt = "تو یک قاضی با دقت هستی"
        prompt = f"""
            بر اساس سوال داده شده بگو که آیا دو جوابی که در ادامه آماده است باهم برابر هستند یا خیر؟

            سوال: {question}
            جواب۱ :{correct_answer}
            جواب۲: {predicted_answer}

            با 0 یا 1 جواب بده و چیز دیگری نگو
            """
         
        response = self.judge.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    
    def check_validation(self, row):
         
        question = row[self.question_c]
        correct_answer = row[self.correct_answer_c]
        predicted_answer = row[self.predicted_answer_c]

        judge_response = self.ask_judge(question, correct_answer, predicted_answer)

        if judge_response == 'بله':
            return 1
        
        elif judge_response == 'خیر':
            return 0
        
        else:
            return judge_response
    
    def calculate_accuracy(self):
          
        csv = pd.read_csv(self.csv_path)
        csv['result'] = csv.progress_apply(self.check_validation, axis=1)
        csv['result'] = pd.to_numeric(csv['result'], errors='coerce')
        accuracy = csv['result'].mean()

        print(self.model_name, "accuracy is:", f"{accuracy:.2f}%")

        nan_values = csv['result'].isna().sum()

        if nan_values > 0 :
            print('Careful, there are some Nan values in the judge assessment, count =', nan_values)

        return accuracy, csv
