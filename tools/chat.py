def update_chat_history(role: str, content: str, old_chat_history: str) -> str:
    old_chat_history += role + ": \n"
    old_chat_history += content + "\n"
    return old_chat_history

def save_chat_log_to_file(chat_log: str, filename="latest_chat_log.txt", file_path="./"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(chat_log)
