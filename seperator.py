import os

def generate_markdown_link(problem_name, filepath):
    """
    Generates a Markdown link for a given problem name and file path.

    Args:
        problem_name (str): The name of the problem.
        filepath (str): The path to the problem file.

    Returns:
        str: A Markdown link.
    """
    return f"[{problem_name}]({filepath})"

def generate_category_content(problems, difficulty):
    """
    Generates the content for a single category within a difficulty level.

    Args:
        problems (list): A list of tuples, where each tuple contains the problem name and full path
        difficulty (str): the difficulty level (Easy, Medium, Hard)

    Returns:
        str: The Markdown content for the category.
    """
    content = ""
    for problem_name, full_path in problems:
        # Create relative path
        parts = full_path.split(os.sep)
        # Construct the relative path.
        relative_path = os.path.join(*parts[1:])
        link = generate_markdown_link(problem_name, relative_path)
        content += f"{link}\n"
    return content

def generate_difficulty_readme(base_dir):
    """
    Generates the README.md files for each difficulty level (Easy, Medium, Hard).

    Args:
        base_dir (str): The base directory of the repository (e.g., "./").
    """
    # Create the dictionary to store the problems
    problems_by_difficulty = {
        "Easy": {},
        "Medium": {},
        "Hard": {},
    }

    # Walk through the directory tree
    for root, dirs, files in os.walk(base_dir):
        #check if the root directory is one of the difficulty levels
        if os.path.basename(root) in ["Easy", "Medium", "Hard"]:
            difficulty_level = os.path.basename(root)
            for filename in files:
                if filename.endswith(".md"):
                    # Get the category.
                    category_name = os.path.basename(os.path.dirname(os.path.join(root, filename)))
                    problem_name = os.path.splitext(filename)[0]  # Remove .md extension
                    full_path = os.path.join(root, filename)

                    if category_name not in problems_by_difficulty[difficulty_level]:
                         problems_by_difficulty[difficulty_level][category_name] = []
                    problems_by_difficulty[difficulty_level][category_name].append((problem_name, full_path))

    # Generate README files for each difficulty level
    for difficulty, categories in problems_by_difficulty.items():
        readme_content = f"# Data Structures and Algorithms Practice - {difficulty} Problems\n\n"
        readme_content += f"This section provides a direct list of all the **{difficulty}** difficulty problems organized by category.\n\n"

        for category, problems in categories.items():
            readme_content += f"## {category}\n\n"
            readme_content += generate_category_content(problems, difficulty) + "\n"

        #create file name
        file_name = f"{difficulty.upper()}_PROBLEMS.md"
        # Write to README file
        with open(file_name, "w") as f:
            f.write(readme_content)
        print(f"Generated {file_name}")

if __name__ == "__main__":
    # The script should be run from the root of your repository.
    base_dir = "./"  # Adjust this if needed, but usually "./" is correct.
    generate_difficulty_readme(base_dir)
