# examples_loader.py

import os
def load_examples(directory):
    examples = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt") and not filename.endswith("_solution.txt"):
            print("qualifiedfilename =",os.path.join(directory, filename))
            with open(os.path.join(directory, filename), 'r') as file:
                lines = file.readlines()
                print("lines=", lines)
                title = lines[0].replace("# Title: ", "").strip()
                description = lines[1].replace("# Description: ", "").strip()
                code = "".join(lines[2:]).strip()

            solution_filename = filename.replace(".txt", "_solution.txt")
            with open(os.path.join(directory, solution_filename), 'r') as file:
                solution_lines = file.readlines()
                refactored_code = "".join(solution_lines[2:]).strip()

            examples.append({
                "title": title,
                "description": description,
                "code": code,
                "refactored_code": refactored_code
            })
    return {"examples": examples}
