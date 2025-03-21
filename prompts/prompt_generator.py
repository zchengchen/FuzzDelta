from langchain.prompts import PromptTemplate

class PromptGenerator:
    def request_analysis_template(self, commit_diff: str) -> str:
        template = f"""\
            You are an expect to help detecting vulnerabilities introduced by commits. The commit information is shown as follows:
            {commit_diff}
            Does this commit introduce any new vulnerability? If this commit has new vulnerability, please tell me 'YES' in the first line and analyze the cause in the followings. Otherwise, please return 'NO'.
            Your cause should contain the following information:
            (1) Why this commit is vulnerable?
            (2) Under what conditions does the input trigger this vulnerability? The more detailed, the better.
        """
        return template
    
    def request_existing_harness_template(self, existing_harness_info: str) -> str:
        template = f"""\
            You need to choose the one you need from the following harness and I will give you the file name and function description. Then tell me the filename you need. Just tell me the filename, no additional explanation or output is needed.
            {existing_harness_info}\
        """
        return template


    def request_modified_harness_template(self, commit_diff: str, analysis: str, harness_impl: str) -> str:
        template = f"""\
            The commit information is shown as follows:
            {commit_diff}
            Your analysis about how to trigger the vulnerability before:
            {analysis}
            The implementation of harness you need is shown as follows:
            {harness_impl}
            Now you need to modify this code to make fuzzing more efficient. Specifically, you should:
            1. Generate an input that can reach the vulnerable function.
            2. Analyze which part of the input can trigger this vulnerability (we called the part that trigger the vulnerability as critical part)?
            3. Keep remaining part fixed in fuzz driver. Let input generated by libFuzzer to fill the critical part.
            4. Keep as many parts of the input unrelated to triggering the vulnerability unchanged as possible.
            5. You can only modify the content inside the LLVMFuzzerTestOneInput function. Do not introduce additional dependencies that may cause compilation failure. Do not change other functions outside LLVMFuzzerTestOneInput. The function must be returned in its entirety, and it should be ready to use as-is.
            6. Generate some inputs as corpus to make fuzzing more efficient.
        """
        return template

if __name__ == "__main__":
    prompt_gen = PromptGenerator()
    print(prompt_gen.request_analysis_template("{commit_diff}"))
    print("===")
    print(prompt_gen.request_existing_harness_template("{harness_info}"))
    print("===")
    print(prompt_gen.request_existing_harness_template("{harness_impl}"))