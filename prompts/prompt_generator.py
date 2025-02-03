from langchain.prompts import PromptTemplate
import textwrap

class PromptGenerator:
    def gen_driver_template(self, api_name: str, api_document: str, api_example: str) -> str:
        template = textwrap.dedent("""
            
        """)
        return template
    

if __name__ == "__main__":
    prompt_gen = PromptGenerator()
    print(prompt_gen.gen_driver_template("", "", ""))