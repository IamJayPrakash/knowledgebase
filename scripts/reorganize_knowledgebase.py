# -*- coding: utf-8 -*-
"""
Reorganizes the knowledge base into the 16-Tier Clean Architecture:
01-web-core-and-performance
02-javascript
03-typescript
04-react
05-angular-21
06-nextjs
07-backend-node
08-backend-python-fastapi
09-backend-java-springboot
10-backend-ruby-and-stacks
11-databases-and-caching
12-ai-and-genai
13-system-design
14-leetcode-blind-75
15-testing-and-devops
16-interview-master-guides
"""

import os
import shutil
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_cmd(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Warning: {res.stderr.strip()}")
    return res

def move_path(src, dst):
    src_path = os.path.join(BASE_DIR, src)
    dst_path = os.path.join(BASE_DIR, dst)
    if os.path.exists(src_path):
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        # Use git mv if possible, else shutil.move
        res = run_cmd(f'git mv "{src}" "{dst}"')
        if res.returncode != 0:
            shutil.move(src_path, dst_path)
            print(f"Fallback moved: {src} -> {dst}")
        else:
            print(f"Git moved: {src} -> {dst}")

def main():
    print("Beginning Knowledge Base Reorganization...")

    # Step 1: 01-core-web-and-performance -> 01-web-core-and-performance
    move_path("01-core-web-and-performance", "01-web-core-and-performance")

    # Step 2: 01-javascript -> 02-javascript
    move_path("01-javascript", "02-javascript")

    # Step 3: 02-typescript -> 03-typescript
    move_path("02-typescript", "03-typescript")

    # Step 4: 03-react -> 04-react
    move_path("03-react", "04-react")

    # Step 5: 04-frontend-frameworks/angular -> 05-angular-21
    move_path("04-frontend-frameworks/angular", "05-angular-21")

    # Step 6: 04-frontend-frameworks/nextjs -> 06-nextjs
    move_path("04-frontend-frameworks/nextjs", "06-nextjs")

    # Remove empty 04-frontend-frameworks if exists
    ff_dir = os.path.join(BASE_DIR, "04-frontend-frameworks")
    if os.path.exists(ff_dir) and not os.listdir(ff_dir):
        os.rmdir(ff_dir)

    # Step 7: 04-node -> 07-backend-node
    move_path("04-node", "07-backend-node")
    # Move node-express into 07-backend-node/express
    move_path("05-backend-and-runtimes/node-express", "07-backend-node/express")

    # Step 8: 05-fastapi -> 08-backend-python-fastapi
    move_path("05-fastapi", "08-backend-python-fastapi")

    # Step 9: 05-backend-and-runtimes/java-springboot -> 09-backend-java-springboot
    move_path("05-backend-and-runtimes/java-springboot", "09-backend-java-springboot")

    # Step 10: 05-backend-and-runtimes/ruby-on-rails and mean-vs-mern -> 10-backend-ruby-and-stacks
    move_path("05-backend-and-runtimes/ruby-on-rails", "10-backend-ruby-and-stacks/ruby-on-rails")
    move_path("05-backend-and-runtimes/mean-vs-mern", "10-backend-ruby-and-stacks/mean-vs-mern")

    # Remove empty 05-backend-and-runtimes if exists
    br_dir = os.path.join(BASE_DIR, "05-backend-and-runtimes")
    if os.path.exists(br_dir) and not os.listdir(br_dir):
        os.rmdir(br_dir)

    # Step 11: 06-databases-and-caching -> 11-databases-and-caching
    move_path("06-databases-and-caching", "11-databases-and-caching")

    # Step 12: 06-ai-genai -> 12-ai-and-genai
    move_path("06-ai-genai", "12-ai-and-genai")

    # Step 13: 07-system-design -> 13-system-design
    move_path("07-system-design", "13-system-design")

    # Step 14: 08-leetcode-dsa -> 14-leetcode-blind-75
    move_path("08-leetcode-dsa", "14-leetcode-blind-75")

    # Step 15: 10-testing-and-devops -> 15-testing-and-devops
    move_path("10-testing-and-devops", "15-testing-and-devops")

    # Step 16: 09-interview-cheatsheet and 11-interview-master-cheatsheets -> 16-interview-master-guides
    move_path("11-interview-master-cheatsheets", "16-interview-master-guides")
    # Move files from 09-interview-cheatsheet into 16-interview-master-guides
    ics_dir = os.path.join(BASE_DIR, "09-interview-cheatsheet")
    if os.path.exists(ics_dir):
        for item in os.listdir(ics_dir):
            src_item = f"09-interview-cheatsheet/{item}"
            dst_item = f"16-interview-master-guides/{item}"
            move_path(src_item, dst_item)
        if os.path.exists(ics_dir) and not os.listdir(ics_dir):
            os.rmdir(ics_dir)

    print("Knowledge base reorganization complete!")

if __name__ == "__main__":
    main()
