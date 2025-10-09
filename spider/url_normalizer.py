from urllib.parse import urlparse, unquote

def normalize_url(url):
    # Parse URL parts
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')  # remove 'www.'
    
    # Decode Persian (or other encoded) characters
    path = unquote(parsed.path)
    
    # Split into parts (remove empty ones)
    parts = [p for p in path.split('/') if p]
    
    # If it has at least 2 parts, combine the last two
    if len(parts) >= 2:
        parts[-2] = f"{parts[-2]}-{parts[-1]}"
        parts = parts[:-1]  # remove the last element (already merged)
    
    # Reconstruct path
    new_path = '/'.join(parts)
    
    # Build final URL
    return f"{domain}/{new_path}"