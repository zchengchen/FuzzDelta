import json
import re

def get_commits_history(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        commits_history = json.load(file)
    return commits_history

def get_commit_detail(commits_info, commit_hash: str):
    for commit in commits_info:
        if commit_hash == commit["commit_sha"]:
            return commit
    raise ValueError(f"Commit hash '{commit_hash}' not found in commits_info.")

def get_file_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def extract_fuzzer_function(code: str) -> str:
    pattern = re.compile(
        r'int\s+LLVMFuzzerTestOneInput\s*\(\s*const\s+uint8_t\s*\*\s*data,\s*size_t\s*size\s*\)\s*\{'
        r'(.*?)'
        r'\n\}',
        re.DOTALL
    )
    match = pattern.search(code)
    return match.group(0) if match else None

def replace_fuzzer_function(file_path: str, new_fuzz_func: str):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    pattern = re.compile(
        r'int\s+LLVMFuzzerTestOneInput\s*\(\s*const\s+uint8_t\s*\*\s*data,\s*size_t\s*size\s*\)\s*\{'
        r'(.*?)'
        r'\n\}',
        re.DOTALL
    )

    if not pattern.search(code):
        raise ValueError("Error: LLVMFuzzerTestOneInput function not found in the file!")

    new_fuzz_func_escaped = re.escape(new_fuzz_func)
    updated_code = pattern.sub(new_fuzz_func_escaped, code)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_code)

if __name__ == "__main__":
    print(extract_fuzzer_function(get_file_content("/home/zhicheng/FuzzDelta/experiments/aixcc_nginx/src/harnesses/pov_harness.cc")))