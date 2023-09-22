import openai
openai.api_key_path = "./key.txt"

class assist:
    def __init__(self):
        self.text = [
            {"role": "system","content":"You are a helpful assistant"}
        ]

    def response(self,user_text:str):
        self.user_text = user_text
       
        while True:

            if self.user_text == "stop":
                break

            self.text.append({"role":"user","content":self.user_text})
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = self.text
            )
            return response['choices'][0]['message']['content']
