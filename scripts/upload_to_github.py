import os
import base64
import requests
import json
from pathlib import Path
import sys

GITHUB_REPO = "ydhqj211-stack/mm"
REPO_PATH = Path(__file__).parent.parent

token = sys.argv[1] if len(sys.argv) > 1 else input("Enter your GitHub Personal Access Token: ").strip()

if not token:
    print("Token is required!")
    exit(1)

def get_sha(repo_path, branch, file_path):
    url = f"https://api.github.com/repos/{repo_path}/contents/{file_path}?ref={branch}"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('sha')
    return None

def upload_file(repo_path, branch, file_path, content):
    url = f"https://api.github.com/repos/{repo_path}/contents/{file_path}"
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    payload = {
        'message': f'Add {file_path}',
        'content': encoded_content,
        'branch': branch
    }

    sha = get_sha(repo_path, branch, file_path)
    if sha:
        payload['sha'] = sha

    response = requests.put(url, headers=headers, json=payload)
    return response.status_code in [200, 201], response.status_code, response.text

branch = "main"
success_count = 0
fail_count = 0

exclude_patterns = {'.git', '__pycache__', 'build', '.gradle', 'bin', '.idea', '.vscode'}

files_to_upload = []
for root, dirs, files in os.walk(REPO_PATH):
    dirs[:] = [d for d in dirs if d not in exclude_patterns]
    for file in files:
        full_path = Path(root) / file
        relative_path = full_path.relative_to(REPO_PATH)
        if str(relative_path).startswith('.github'):
            continue
        files_to_upload.append((str(relative_path).replace('\\', '/'), full_path))

workflow_path = REPO_PATH / '.github' / 'workflows' / 'build.yml'
if workflow_path.exists():
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow_content = f.read()
    success, status, resp = upload_file(GITHUB_REPO, branch, '.github/workflows/build.yml', workflow_content)
    print(f"[{'OK' if success else 'FAIL'}] .github/workflows/build.yml (status: {status})")
    if success:
        success_count += 1
    else:
        fail_count += 1
        print(f"    Response: {resp[:200]}")

print(f"Found {len(files_to_upload)} files to upload")
print()

for relative_path, full_path in files_to_upload:
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        success, status, resp = upload_file(GITHUB_REPO, branch, relative_path, content)
        print(f"[{'OK' if success else 'FAIL'}] {relative_path} (status: {status})")
        if success:
            success_count += 1
        else:
            fail_count += 1
            if status == 401:
                print(f"    ERROR: Invalid token or insufficient permissions")
            elif status == 404:
                print(f"    ERROR: Repository not found or file path issue")
    except Exception as e:
        print(f"[ERROR] {relative_path}: {e}")
        fail_count += 1

print()
print("=" * 50)
print(f"Upload complete! Success: {success_count}, Failed: {fail_count}")
print("=" * 50)

if fail_count > 0:
    print()
    print("If all failed, please check:")
    print("1. Your Personal Access Token is valid")
    print("2. Token has 'repo' scope (for private repos)")
    print("3. Repository exists: https://github.com/ydhqj211-stack/mm")