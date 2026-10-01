"""
update_readme_with_ai.py
Scans the local repository directory, summarizes structural changes, 
and uses the Gemini API to update README.md automatically.
"""
import os
from google import genai
import warnings

# Try loading .env variables automatically
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

warnings.filterwarnings("ignore")

def get_api_key() -> str:
    """Retrieves the Gemini API key from environment variables or .env file."""
    candidate_keys = ["Gemini_Reanalysis", "GEMINI_API_KEY"]
    for key_name in candidate_keys:
        api_key = os.environ.get(key_name)
        if api_key:
            return api_key

    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line_str = line.strip()
                if line_str and not line_str.startswith("#"):
                    for key_name in candidate_keys:
                        if line_str.startswith(f"{key_name}="):
                            parts = line_str.split("=", 1)
                            if len(parts) == 2:
                                val = parts[1].strip().strip('"').strip("'")
                                if val:
                                    return val
    return None

def scan_repository_structure(root_dir: str = ".") -> str:
    """Walks through the repository directory and generates a text tree structure."""
    ignore_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'trade500', 'daily_signals', 'tickers'}
    ignore_extensions = {'.pyc', '.png', '.jpg', '.m4a', '.csv'}
    
    tree_lines = []
    tree_lines.append(f"{os.path.basename(os.path.abspath(root_dir))}/")
    
    for root, dirs, files in os.walk(root_dir):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        relative_path = os.path.relpath(root, root_dir)
        indent_level = 0 if relative_path == '.' else relative_path.count(os.sep) + 1
        indent = "│   " * indent_level
        
        if relative_path != '.':
            tree_lines.append(f"{indent}├── {os.path.basename(root)}/")
            
        sub_indent = "│   " * (indent_level + 1)
        for file in sorted(files):
            if any(file.endswith(ext) for ext in ignore_extensions):
                continue
            if file.startswith('.'):
                continue
            tree_lines.append(f"{sub_indent}├── {file}")
            
    return "\n".join(tree_lines)

def main():
    api_key = get_api_key()
    if not api_key:
        print("[!] Error: Could not locate Gemini API key in .env or environment variables.")
        return

    client = genai.Client(api_key=api_key)

    print("[+] Scanning repository directory structure...")
    current_structure = scan_repository_structure()

    readme_path = "README.md"
    current_readme = ""
    if os.path.exists(readme_path):
        print(f"[+] Loading existing '{readme_path}'...")
        with open(readme_path, "r", encoding="utf-8") as f:
            current_readme = f.read()
    else:
        print(f"[-] Warning: '{readme_path}' not found. Generating a new one from scratch.")

    print("[+] Transmitting file structure and README context to Gemini for synchronization...")

    prompt = f"""
    You are an expert technical writer and lead quantitative software architect.
    
    I need you to update and synchronize our project's `README.md` file based on the actual current file structure of the repository.
    
    ---
    CURRENT REPOSITORY FILE STRUCTURE:
    {current_structure}
    ---
    
    CURRENT README.md CONTENT:
    {current_readme}
    ---
    
    Task:
    1. Analyze the repository file structure and compare it against the current `README.md`.
    2. Document any updates, new strategy pods, files, or folder structures present in the repository scan.
    3. Rewrite/Update the `README.md` completely so that the directory tree, strategy descriptions, system architecture, and command references match the actual codebase precisely.
    4. Keep the professional Markdown layout, emojis, and clear section dividers.
    
    CRITICAL: Return ONLY the raw, updated Markdown content for the README. Do not wrap the final output in conversational filler text outside of the Markdown layout (you may use standard markdown block formatting or output it cleanly).
    """

    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )

    updated_content = response.text.strip()
    
    # Strip accidental code block markdown wrappers if Gemini returns them around the whole payload
    if updated_content.startswith("```markdown"):
        updated_content = updated_content[len("```markdown"):]
    elif updated_content.startswith("```"):
        updated_content = updated_content[len("```"):]
    if updated_content.endswith("```"):
        updated_content = updated_content[:-3]
    updated_content = updated_content.strip()

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"\n✅ SUCCESS: '{readme_path}' has been successfully updated and synchronized with your repository structure!")

if __name__ == "__main__":
    main()