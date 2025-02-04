from langchain.prompts import PromptTemplate
import textwrap

class PromptGenerator:
    def gen_driver_template(self, project_name: str, api_name: str, api_document: str, api_example: str) -> str:
        template = textwrap.dedent(f"""
Perform fuzz testing on the {project_name}'s API: {api_name}. The API details are as follows:
{api_document}

An example usage of this API is as follows:
{api_example}
Generate a fuzzing driver for Libfuzzer. A fuzzing harness that exercises the API correctly.
You just need to give me the fuzzing harness code. Do not contain other insturction, or other special characters such as ```
        """)
        return template
    
    def report_error_template(self, bug_report) -> str:
        template = textwrap.dedent(f"""
The code you provided caused the following error during the clang++ compilation process. 
{bug_report}
Please fix it and return the corrected code directly. 
Do not include any other instructions or special characters such as ```.
        """)
        return template
    

if __name__ == "__main__":
    prompt_gen = PromptGenerator()
    print(prompt_gen.gen_driver_template("", "", ""))