import os

def build_gallery(base_dir="interactive"):
    files_by_dir = {}
    gantt_files_global = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(base_dir):
        # Find all HTML files, exclude the index.html we are about to create
        raw_files = [f for f in files if f.endswith('.html') and f != 'index.html']
        
        rel_dir = os.path.relpath(root, base_dir).replace('\\', '/')
        if rel_dir == '.':
            rel_dir = 'Root'
            
        for file in sorted(raw_files, key=str.lower):
            file_path = file if rel_dir == 'Root' else f"{rel_dir}/{file}"
            # Clean up filename for nicer display and remove leading/trailing whitespace
            display_name = file.replace('.html', '').replace('_', ' ').strip()
            
            if 'gantt' in file.lower():
                gantt_files_global.append((file_path, display_name))
            else:
                if rel_dir not in files_by_dir:
                    files_by_dir[rel_dir] = []
                files_by_dir[rel_dir].append((file_path, display_name))

    # Define explicit order for specific folders, others will follow alphabetically
    folder_priority = {
        'CP+GWS': 1,
        'CP+RDI': 2,
        'Root': 3
    }
    
    # Sort the directories using the explicit priority first, then alphabetical
    def get_sort_key(dir_name):
        priority = folder_priority.get(dir_name, 999) # 999 for anything not explicitly ordered
        return (priority, dir_name.lower())

    sorted_dirs = sorted(files_by_dir.keys(), key=get_sort_key)

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Figures Gallery</title>
    <style>
        body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; display: flex; height: 100vh; overflow: hidden; background-color: #f8f9fa; }
        #sidebar { width: 320px; background-color: #212529; color: #fff; overflow-y: auto; display: flex; flex-direction: column; flex-shrink: 0; }
        #sidebar-header { padding: 20px; background: #1a1d20; border-bottom: 1px solid #343a40; }
        #sidebar h2 { font-size: 1.2rem; margin: 0; color: #f8f9fa; letter-spacing: 0.5px; }
        .category { margin-top: 15px; }
        .category-title { font-weight: bold; padding: 8px 20px; background: #343a40; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; color: #adb5bd; position: sticky; top: 0; z-index: 2; }
        .file-list { list-style: none; padding: 0; margin: 0; }
        .file-link { display: block; padding: 10px 20px 10px 25px; color: #ced4da; text-decoration: none; font-size: 0.85rem; line-height: 1.4; word-break: break-word; transition: all 0.2s; border-left: 3px solid transparent; }
        .file-link:hover { background-color: #343a40; color: #fff; }
        .file-link.active { background-color: #495057; color: #fff; border-left-color: #0d6efd; font-weight: 500; }
        #main { flex-grow: 1; display: flex; flex-direction: column; background: #fff; }
        #header { padding: 15px 25px; background: #fff; border-bottom: 1px solid #dee2e6; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); z-index: 10; }
        #current-title { margin: 0; font-size: 1.1rem; color: #212529; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 70%; }
        #open-new { color: #0d6efd; text-decoration: none; font-size: 0.9rem; font-weight: 500; display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; border-radius: 4px; transition: background 0.2s; }
        #open-new:hover { background: #f8f9fa; text-decoration: none; }
        iframe { flex-grow: 1; border: none; width: 100%; height: 100%; background: #f8f9fa; }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.4); }
        #main ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.2); }
        #main ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.4); }
    </style>
</head>
<body>
    <div id="sidebar">
        <div id="sidebar-header">
            <h2>Figures Gallery</h2>
        </div>
"""

    # Add Gantt charts as their own dedicated section at the very top
    if gantt_files_global:
        # Sort Gantt charts in reverse so that small comes before medium before large
        gantt_files_global.sort(key=lambda x: x[1], reverse=True)
        
        html_content += f'        <div class="category">\n'
        html_content += f'            <div class="category-title" style="background: #0d6efd; color: white;">Gantt Charts</div>\n'
        html_content += f'            <ul class="file-list">\n'
        for file_path, display_name in gantt_files_global:
            html_content += f'                <li><a href="#{file_path}" class="file-link" data-src="{file_path}">{display_name}</a></li>\n'
        html_content += f'            </ul>\n'
        html_content += f'        </div>\n'

    for directory in sorted_dirs:
        html_content += f'        <div class="category">\n'
        html_content += f'            <div class="category-title">{directory}</div>\n'
        html_content += f'            <ul class="file-list">\n'
        for file_path, display_name in files_by_dir[directory]:
            html_content += f'                <li><a href="#{file_path}" class="file-link" data-src="{file_path}">{display_name}</a></li>\n'
        html_content += f'            </ul>\n'
        html_content += f'        </div>\n'

    html_content += """    </div>
    <div id="main">
        <div id="header">
            <h3 id="current-title">Select a figure from the menu</h3>
            <a id="open-new" href="#" target="_blank" style="display: none;">
                Open in new tab 
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
            </a>
        </div>
        <iframe id="figure-frame" src=""></iframe>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const iframe = document.getElementById('figure-frame');
            const title = document.getElementById('current-title');
            const openNew = document.getElementById('open-new');
            const links = document.querySelectorAll('.file-link');

            function loadFigureFromHash() {
                let hash = window.location.hash.substring(1);
                
                // If no hash, default to the first link
                if (!hash) {
                    if (links.length > 0) {
                        hash = links[0].getAttribute('data-src');
                        // Use replaceState to avoid cluttering history with the default load
                        history.replaceState(null, null, '#' + hash);
                    } else {
                        return;
                    }
                }

                // Update UI: highlight active link in sidebar
                links.forEach(l => l.classList.remove('active'));
                const activeLink = Array.from(links).find(l => l.getAttribute('data-src') === hash);
                
                if (activeLink) {
                    activeLink.classList.add('active');
                    title.textContent = activeLink.textContent;
                    
                    // Only scroll into view if it's not already visible
                    const rect = activeLink.getBoundingClientRect();
                    const sidebar = document.getElementById('sidebar');
                    if (rect.top < sidebar.offsetTop || rect.bottom > (sidebar.offsetTop + sidebar.offsetHeight)) {
                        activeLink.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }
                } else {
                    title.textContent = hash.split('/').pop().replace('.html', '').replace(/_/g, ' ');
                }

                // Load iframe and update external link
                iframe.src = hash;
                openNew.href = hash;
                openNew.style.display = 'inline-flex';
            }

            // Listen for hash changes (back/forward buttons, manual URL edit)
            window.addEventListener('hashchange', loadFigureFromHash);

            // Initial load
            loadFigureFromHash();
        });
    </script>
</body>
</html>
"""

    out_path = os.path.join(base_dir, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Gallery successfully generated at {out_path} with {sum(len(files) for files in files_by_dir.values())} figures.")

if __name__ == "__main__":
    build_gallery()
