import concurrent.futures
import subprocess

def run_script(script_name):
    command = f"python3 {script_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Output of {script_name}:\n{result.stdout}")

if __name__ == "__main__":
    scripts = ["robot_arm.py", "model_gui.py"]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_script, scripts)
