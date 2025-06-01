import os
import shutil
import stat
from block import markdown_to_html_node

def on_rm_error(func, path, exc_info):
    # Cambia permisos y vuelve a intentar
    os.chmod(path, stat.S_IWRITE)
    func(path)


def static_to_public():
    #
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    STATIC_DIR= os.path.join(BASE_DIR, "static")
    PUBLIC_DIR= os.path.join(BASE_DIR, "public")
    #
    if os.path.exists(PUBLIC_DIR):
        shutil.rmtree(PUBLIC_DIR, onexc=on_rm_error)
        #
        os.mkdir(PUBLIC_DIR)    
    #
    copy_static_content(STATIC_DIR,PUBLIC_DIR)


def copy_static_content(from_path, to_path):
    contents = os.listdir(from_path)
    if not contents:
        return
    
    for content in contents:
        from_rute_path = os.path.join(from_path, content)
        to_rute_path = os.path.join(to_path, content)
        if os.path.isfile(from_rute_path):
            shutil.copy(from_rute_path, to_path)
        else:
            os.mkdir(to_rute_path)
            copy_static_content(from_rute_path, to_rute_path)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("There is no main header: h1")


def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating from {from_path} to {dest_path} using {template_path}")

    with open(from_path,"r") as file:
        markdown_file = file.read()

    with open(template_path,"r") as file:
        template_file = file.read()

    html_node = markdown_to_html_node(markdown_file)
    html_title = extract_title(markdown_file)
    
    template_file = template_file.replace("{{ Title }}", html_title)
    template_file = template_file.replace("{{ Content }}", html_node.to_html())
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as file:
        file.write(template_file)

    
def generate_page_recursively(dir_path_content, template_path, dest_dir_path):
    dir_entries = os.listdir(dir_path_content)

    for entry in dir_entries:
        if os.path.isfile(os.path.join(dir_path_content,entry)):
            generate_page(os.path.join(dir_path_content,entry),template_path,os.path.join(dest_dir_path,entry.replace(".md",".html")))
        else:
            generate_page_recursively(os.path.join(dir_path_content,entry),template_path,os.path.join(dest_dir_path,entry))
    return 

def main():
    static_to_public()
    # generate_page("content/index.md","template.html","public/index.html")
    generate_page_recursively("content/","template.html","public/")

if __name__ == "__main__":
    main()