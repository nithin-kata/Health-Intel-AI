import subprocess, os

REPO = r"c:\Users\NITHIN KATA\.gemini\antigravity\scratch\healthcare_intelligence_ai"

def run(cmd):
    print(f">>> {cmd}")
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, shell=True)
    if r.stdout.strip(): print(r.stdout.strip())
    if r.stderr.strip(): print(r.stderr.strip())
    return r.returncode

# Create .gitignore
gitignore_path = os.path.join(REPO, ".gitignore")
if not os.path.exists(gitignore_path):
    with open(gitignore_path, "w") as f:
        f.write("venv/\n__pycache__/\n*.pyc\n*.db\nstatic/groq_test_status.json\nstatic/search_911_results.json\nstatic/git_push_status.json\npush_to_github.bat\n")
    print("Created .gitignore")

run("git init")
run('git config user.email "patient@healthintel.ai"')
run('git config user.name "Health Intel Developer"')
run("git remote remove origin")
run("git remote add origin https://github.com/nithin-kata/Health-Intel-AI.git")
run("git add .")
run('git commit -m "Visual Redesign: Glassmorphism Overhaul, LPU Telemetry & 108 Emergency"')
rc = run("git push -u origin main --force")
if rc != 0:
    run("git branch -M main")
    run("git push -u origin main --force")
print("\nDone!")
