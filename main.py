from prompts.prompt_generator import *
from models.gpto1_chain import *
from tools.common import *
from tools.chat import *
import os
import subprocess
import textwrap
import json

gpto1 = GPTo1Chain()
prompt_gen = PromptGenerator()

vuln_list = {
    "cpv1": "d030af5eb4c64470c8fd5a87a8f6aae547580aa3",
    # "cpv2": "0dbd46415432759475e6e4bb5adfaada6fb7d506",
    # "cpv3": "c502a1695c0e9d0345101a5f2a99ee0e3c890a4d",
    # "cpv4": "b9d6a2caf41565fb05c010ad0c8d2fd6bd3c4c42",
    # "cpv5": "b101d59b3dda654dee1deabc34816e2ca7c96d38",
    # "cpv8": "cf6f5b1d4d85c98b4e2e2fb6f694f996d944851a",
    # "cpv9": "cc4b16fc10dcc579d5f697f3ff70c390b5e7c7d2",
    # "cpv10": "dcf9f055bf1863555869493d5ac5944b5327f128",
    # "cpv11": "a2f5fad3ef16615ed23d21264560748cdc21a385",
    # "cpv12": "348b50dbb52e7d6faad7d75ce9331dd9860131c4",
    # "cpv13": "316d57f895c4c915c5ce3af8b09972d47dd9984e",
    # "cpv14": "9c5e32dcd9779c4cfe48c5377d0af8adc52a2be9",
    # "cpv15": "ef970a54395324307fffd11ab37266479ac37d4c",
    # "cpv17": "b6c0a37554e300aa230ea2b8d7fe53dd8604f602"
}
commits_info_path = "/home/zhicheng/FuzzDelta/experiments/aixcc_nginx/commits.json"
fuzz_drivers_path = "/home/zhicheng/FuzzDelta/experiments/aixcc_nginx/src/harnesses/"
existing_harness_info = """\
    1. pov_harness.cc
        vulnerabilities are primarily related to the request processing chain. Throughout the HTTP request's lifecycle from reception to response, issues may arise in request method parsing, URI normalization, header key-value parsing, route rule matching, and proxy configuration forwarding. Buffer overflows, memory leaks, or logical vulnerabilities are particularly likely when handling headers of abnormal length, malformed URIs, special cookie values, complex location configurations, or multi-layer proxy forwarding.
    2. mail_request_harness.cc
        vulnerabilities are mainly associated with state transitions and authentication flows. The authentication process involves interaction with the auth server (auth_http handling), authentication state validation (auth_done state), and result processing. As a stateful protocol, POP3 must strictly transition between AUTHORIZATION, TRANSACTION, and UPDATE states, each with its specific command set. Improper state transition handling or authentication flow flaws can lead to unauthorized access or state confusion.
    3. smtp_harness.cc
        vulnerabilities primarily relate to command processing and session management. The SMTP server must handle a series of commands from HELO/EHLO to MAIL FROM, RCPT TO, and DATA, each with its specific format and processing logic. Session states must maintain correct transitions from connection initialization through authentication to mail transfer. Security issues can particularly arise during long mail content processing, concurrent connections, or complex authentication scenarios due to incorrect command parsing or state management.\
"""

commits_history = get_commits_history(commits_info_path)

for cpv_name, commit_hash in vuln_list.items():
    chat_history = ""
    commit_info = get_commit_detail(commits_history, commit_hash)
    commit_diff = commit_info["commit_diff"]
    request_analysis_prompt = prompt_gen.request_analysis_template(commit_diff)
    llm_analysis = gpto1.invoke(request_analysis_prompt)
    print(f"[*] {cpv_name} analysis finished.")
    chat_history = update_chat_history("Human", request_analysis_prompt, chat_history)
    chat_history = update_chat_history("LLM", llm_analysis, chat_history)
    if "YES" in llm_analysis:
        print(f"[*] {cpv_name} is suspicious.")
        request_choosing_harness_prompt = prompt_gen.request_existing_harness_template(existing_harness_info)
        chat_history = update_chat_history("Human", request_choosing_harness_prompt, chat_history)
        selected_driver = gpto1.invoke(chat_history)
        chat_history = update_chat_history("LLM", selected_driver, chat_history)
        print("[*] Fuzz driver selection finished.")
        fuzz_driver = get_file_content(os.path.join(fuzz_drivers_path, selected_driver))
        request_modified_driver_prompt = prompt_gen.request_modified_harness_template(llm_analysis, fuzz_driver)
        response = gpto1.invoke(request_modified_driver_prompt)
        chat_history = update_chat_history("Human", request_modified_driver_prompt, chat_history)
        chat_history = update_chat_history("LLM", response, chat_history)
        new_fuzz_func = extract_fuzzer_function(response)
        replace_fuzzer_function(os.path.join(fuzz_drivers_path, selected_driver), new_fuzz_func)
        save_chat_log_to_file(chat_history, f"{cpv_name}_chat_log.txt")
    else:
        print(f"[*] No vulnerability detected in {cpv_name}.")
        
