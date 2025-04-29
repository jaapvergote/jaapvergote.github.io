import os
import re

def add_prompts_nav(content):
    # Find the navigation section
    nav_pattern = r'(<a class="active" href="../blog.html">Blog</a>)\s*(<a class="icon")'
    replacement = r'\1\n<a href="../prompts.html">Prompts</a>\n\2'
    return re.sub(nav_pattern, replacement, content)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated_content = add_prompts_nav(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)

def main():
    posts_dir = 'posts'
    for filename in os.listdir(posts_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(posts_dir, filename)
            process_file(filepath)

if __name__ == '__main__':
    main() 