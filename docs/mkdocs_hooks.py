import re, os


def python_indent(content):
    """ Pattern: classic markdown indent (2 spaces) to Python-Markdown indent (4 spaces)
        Handle both single and double indent. In reverse so we don't overwrite.
    """
    # double
    content = re.sub(r'^(\ \ \ \ -\ .*)', r'    \1', content, flags=re.MULTILINE)
    # single
    content = re.sub(r'^(\ \ -\ .*)', r'  \1', content, flags=re.MULTILINE)

    return content


def on_page_markdown(markdown: str, page, config, files):
    if page.file.src_path == 'index.md':
        readme_path = os.path.join(os.path.dirname(config['config_file_path']), 'README.md')
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Rewrite links: [label](docs/...) -> [label](...)
            # This handles both markdown links [text](url) and images ![text](url)
            # We match (docs/ and replace with (

            # Pattern: parenthesis, docs/, everything else
            content = content.replace('](docs/', '](')

            content = python_indent(content)

            # file paths
            content = content.replace('CONTRIBUTING.md', 'about/contributing.md')
            content = content.replace('CODE_OF_CONDUCT.md', 'about/code_of_conduct.md')

            return content
        except Exception as e:
            print(f"Error including README.md: {e}")
            return markdown

    elif page.file.src_path == 'about/contributing.md':
        # not working yet
        markdown = markdown.replace('CHANGELOG.md', 'about/changelog.md')
        return markdown

    markdown = python_indent(markdown)
    return markdown
