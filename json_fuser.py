import re

def fuse_json(target_file_path: str, content_file_path: str, example_name: str):
    target_file_content = ''
    with open(target_file_path) as target_file:
        target_file_content = str.join('', target_file.readlines())
    
    content_file_content = ''
    with open(content_file_path) as content_file:
        content_file_content = str.join('', content_file.readlines())
    
    regex_content = r".*\s*\/\/\s<!-- begin content -->(.*)\/\/\s<!-- end content -->\s*.*"
    res = re.match(regex_content, content_file_content, re.MULTILINE | re.DOTALL)
    content = ''
    if res != None:
        content = res.group(1)
        
    regex_target = fr"\/\/\s<!-- begin {example_name} -->\s*(.*)\s*\/\/\s<!-- end {example_name} -->"
    target_file_content = re.sub(regex_target, f'// <!-- begin {example_name} -->{content}// <!-- end {example_name} -->', target_file_content)
    
    with open(target_file_path, 'w') as target_file:
        target_file.write(target_file_content)
    
        
    
if __name__ == "__main__":
    fuse_json('.vscode/launch.json', './examples/seat-adjuster/.vscode/launch.json', 'examples/seat-adjuster')
