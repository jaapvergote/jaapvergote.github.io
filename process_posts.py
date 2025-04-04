import os
import re
from bs4 import BeautifulSoup
from datetime import datetime

def parse_date_from_filename(filename):
    # Extract date from filename format YYYY-MM-DD
    match = re.match(r'(\d{4}-\d{2}-\d{2})_', filename)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%d')
    return None

def get_title_from_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Try to find the first h1 or h2 tag
    title = soup.find('h1')
    if not title:
        title = soup.find('h2')
    if title:
        return title.get_text().strip()
    return None

def create_blog_post_html(title, date, content):
    with open('posts/template.html', 'r') as f:
        template = f.read()
    
    # Replace placeholders
    post_html = template.replace('[Post Title]', title)
    date_str = date.strftime('%B %d, %Y')
    date_iso = date.strftime('%Y-%m-%d')
    post_html = post_html.replace('Month DD, YYYY', date_str)
    post_html = post_html.replace('YYYY-MM-DD', date_iso)
    
    # Insert content
    soup = BeautifulSoup(post_html, 'html.parser')
    content_div = soup.find('div', class_='post-content')
    if content_div:
        content_soup = BeautifulSoup(content, 'html.parser')
        
        # Extract the actual content we want to keep
        main_content = content_soup.find('div', class_='section-inner')
        if main_content:
            # Remove the title since we already have it at the top
            title_in_content = main_content.find(['h1', 'h2', 'h3'], class_='graf--title')
            if title_in_content:
                title_in_content.decompose()
            
            # Clean up the content
            content_div.clear()
            content_div.append(main_content)
            
            # Add author information if available
            author_link = content_soup.find('a', class_='p-author')
            if author_link:
                footer = soup.new_tag('footer')
                p = soup.new_tag('p')
                p.string = 'By '
                p.append(author_link)
                footer.append(p)
                content_div.append(footer)
    
    return str(soup)

def create_blog_index(posts):
    with open('blog.html', 'r') as f:
        blog_template = f.read()
    
    soup = BeautifulSoup(blog_template, 'html.parser')
    blog_posts_div = soup.find('div', class_='blog-posts')
    if blog_posts_div:
        blog_posts_div.clear()
        
        # Create unordered list
        ul = soup.new_tag('ul', **{'class': 'blog-list'})
        
        # Separate regular posts and VC interviews
        regular_posts = []
        vc_interviews = []
        
        for post in posts:
            # Skip the post we want to remove
            if "I-mentioned-it-in-the-post" in post['filename']:
                continue
                
            # Separate VC interviews from regular posts
            if "Young--Hungry-and-VC-in-NYC" in post['filename']:
                vc_interviews.append(post)
            else:
                regular_posts.append(post)
        
        # Sort regular posts by date (newest first)
        regular_posts.sort(key=lambda x: x['date'], reverse=True)
        
        # Sort VC interviews by date (oldest first to maintain specified order)
        vc_interviews.sort(key=lambda x: x['date'])
        
        # Add regular posts
        for post in regular_posts:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=f"posts/{post['filename']}")
            a.string = post['title']
            li.append(a)
            date_span = soup.new_tag('span', **{'class': 'post-date'})
            date_span.string = f" - {post['date'].strftime('%B %d, %Y')}"
            li.append(date_span)
            ul.append(li)
        
        # Add VC interviews at the bottom
        for post in vc_interviews:
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=f"posts/{post['filename']}")
            a.string = post['title']
            li.append(a)
            date_span = soup.new_tag('span', **{'class': 'post-date'})
            date_span.string = f" - {post['date'].strftime('%B %d, %Y')}"
            li.append(date_span)
            ul.append(li)
        
        blog_posts_div.append(ul)
    
    return str(soup)

def main():
    posts_dir = 'posts'
    posts = []
    
    # Process each HTML file in the posts directory
    for filename in os.listdir(posts_dir):
        if filename.endswith('.html') and not filename.startswith('draft_') and filename != 'template.html':
            filepath = os.path.join(posts_dir, filename)
            
            # Read the original file
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Parse date and title
            date = parse_date_from_filename(filename)
            if not date:
                continue
                
            soup = BeautifulSoup(content, 'html.parser')
            title = get_title_from_content(content)
            if not title:
                continue
            
            # Get the main content
            main_content = ''
            main_element = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
            if main_element:
                main_content = str(main_element)
            else:
                # If no specific content container found, use body content
                body = soup.find('body')
                if body:
                    main_content = ''.join(str(tag) for tag in body.contents)
            
            # Create new blog post HTML
            new_html = create_blog_post_html(title, date, main_content)
            
            # Save the new file
            with open(filepath, 'w') as f:
                f.write(new_html)
            
            # Add to posts list
            posts.append({
                'filename': filename,
                'title': title,
                'date': date
            })
    
    # Update blog index
    blog_html = create_blog_index(posts)
    with open('blog.html', 'w') as f:
        f.write(blog_html)

if __name__ == '__main__':
    main() 