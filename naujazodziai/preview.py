def html_post(text_builder):
    text_bytes = text_builder.build_text().encode('utf-8')
    facets = text_builder.build_facets()
    
    output = ""
    cursor = 0

    for facet in facets:
        output += text_bytes[cursor:facet.index.byte_start].decode('utf-8')
        part = text_bytes[facet.index.byte_start:facet.index.byte_end].decode('utf-8')
        cursor = facet.index.byte_end

        for feature in facet.features:
            match feature.py_type:
                case 'app.bsky.richtext.facet#link':
                    part = f'<a href="{feature.uri}">{part}</a>'
                case 'app.bsky.richtext.facet#tag':
                    part = f'<a href="https://bsky.app/hashtag/{feature.tag}">{part}</a>'
                
        output += part
    
    output += text_bytes[cursor:].decode('utf-8')
    output = output.replace('\n', '<br/>')
    
    return output

def html_posts(text_builders):
    """
    Generates an HTML file with the extracted JSON data.
    """
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-size: 15px;
            font-family: InterVariable, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            line-height: 20px;
            background: #161e27; color: #fff;
        }
        ul { list-style-type: none; padding: 0; width: 515px; margin: auto }
        li { padding: 15px; border: solid 1px #2e4052; border-top: none; }
        li:hover { background: #1e2936 }
        a { text-decoration: none; color: rgb(32, 139, 254) }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <ul>
"""
    
    lines = ["        <li>" + html_post(text_builder) + "</li>" for text_builder in text_builders]
    html_content += "\n".join(lines)

    html_content += """
    </ul>
</body>
</html>
"""
    
    return html_content
