import subprocess

if __name__ == '__main__':
    subprocess.run(["solara", "run", "./uiservice/view/webcat_GUI.py", "--host=0.0.0.0"])


