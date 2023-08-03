import subprocess
from flask import current_app
def run_cpp_program(command):
    # Compile the C++ program
    path = (
        current_app.config["ROOT_PATH"]
        + "\\"
        + "karmalegoweb"
        + "\\"
        + "src"
        + "\\"
        + "negative_mining"
        + "\\"
    )

    NegativeRanges =  path + 'NegativeRanges.cpp'
    Sequence = path + 'Sequence.cpp'
    main = path + 'main.cpp'
    compile = subprocess.run(['g++', NegativeRanges, Sequence, main, '-o', "NegativeRanges"], shell=True)

    # # Run the program
    if compile.returncode == 1:
        return 1
    try:
        proc = subprocess.run(command, timeout=120)
        if proc.returncode == 0:
            return 0
        else:
            return 1
    except subprocess.TimeoutExpired:
        return 0
