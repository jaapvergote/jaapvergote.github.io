#!/bin/bash

for file in posts/*.html; do
  # Create a temporary file
  tmp=$(mktemp)
  
  # Process the file and write to temporary file
  awk '
    # Print everything before the head section
    /^<head>/,/^<\/head>/ {
      if ($0 ~ /^<head>/) {
        print "<head>"
        print "<meta content=\"width=device-width, initial-scale=1.0\" name=\"viewport\"/>"
        print "<meta charset=\"utf-8\"/>"
        print "<link href=\"../style.css\" rel=\"stylesheet\"/>"
        print "<title>" FILENAME " - Jaap Vergote</title>"
        print "<link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap\" rel=\"stylesheet\">"
        print "<link href=\"../images/jaap-profile.jpg\" rel=\"icon\" type=\"image/png\"/>"
        print "<!-- Load an icon library to show a hamburger menu (bars) on small screens -->"
        print "<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css\">"
        print "<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌞</text></svg>\">"
        print "</head>"
        next
      }
      next
    }
    
    # Replace the navigation section
    /^<div class="topnav"/, /^<\/div>/ {
      if ($0 ~ /^<div class="topnav"/) {
        print "<div class=\"topnav\" id=\"myTopnav\">"
        print "  <a href=\"../index.html\">Home</a>"
        print "  <a href=\"../now.html\">Now</a>"
        print "  <a href=\"../about.html\">About</a>"
        print "  <a href=\"../books.html\">Bookshelf</a>"
        print "  <a class=\"active\" href=\"../blog.html\">Blog</a>"
        print "  <a href=\"../prompts.html\">Prompts</a>"
        print "  <a class=\"icon\" href=\"javascript:void(0);\" onclick=\"toggleMenu()\">"
        print "    <i class=\"fa fa-bars\"></i>"
        print "  </a>"
        print "</div>"
        next
      }
      next
    }
    
    # Print everything else as is
    { print }
  ' "$file" > "$tmp"
  
  # Replace original file with updated version
  mv "$tmp" "$file"
done 