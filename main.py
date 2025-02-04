from prompts.prompt_generator import *
from models.gpt4o_chain import *
import subprocess

gpt4o = GPT4oChain()
prompt_gen = PromptGenerator()


document="jpeg_start_decompress() is a function in the libjpeg library that initializes the decompression process after jpeg_read_header(). It sets up output parameters like image dimensions and color space. The function takes a pointer to jpeg_decompress_struct and returns TRUE on success. It must be called before reading scanlines with jpeg_read_scanlines(). After decompression, jpeg_finish_decompress() should be used to finalize the process."
example="""
jpeg_start_decompress(&cinfo);
while (cinfo.output_scanline < cinfo.output_height) {
    jpeg_read_scanlines(&cinfo, buffer, 1);
}
jpeg_finish_decompress(&cinfo);
"""
proj_name="libjpeg"
compile_command = f"clang++ -fsanitize=fuzzer,address -o {proj_name}_driver {proj_name}_driver.c -L./fuzzdelta-libjpeg/bin/lib -ljpeg -Wl,-rpath,./fuzzdelta-libjpeg/bin/lib"

prompt = prompt_gen.gen_driver_template(project_name="libjpeg",
                                        api_name="jpeg_start_decompress",
                                        api_document=document,
                                        api_example=example)

prompt_history = "Human:\n" + prompt + "\n"

while True:
    fuzz_code = gpt4o.invoke(prompt)
    with open(f"{proj_name}_driver.c", "w", encoding="utf-8") as file:
        file.write(fuzz_code)
    prompt_history += "LLM:\n" + fuzz_code + "\n"
    result = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
    if "error" in result.stderr:
        error_report = result.stderr
        prompt = prompt_gen.report_error_template(error_report)
        prompt_history += "Human:\n" + prompt + "\n"
    else:
        break

with open("response.txt", "w", encoding="utf-8") as file:
    file.write(prompt_history)