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
    proc = subprocess.run(['g++', '-o', NegativeRanges, Sequence, main], capture_output=True)
    result = proc.returncode

    print("result is: " + str(result))

    return result

    # # Run the program
    # subprocess.run(command)