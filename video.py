from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def show_video():
    url = request.form.get('url')
    
    html_get_url = """
    <form action="/" method="POST">
    <textarea name="url" rows="5" placeholder="URL" style="width: 90%; font-size: 2em;"></textarea>
    <br><br>
    <input type="submit">
    </form>
    """
    
    html_show_video = f"""
    <video width="100%" height="100%" controls preload="metadata">
        <source src="{url}">
    </video>
    """
    
    if url == None:
        return html_get_url
    return html_show_video

app.run('127.0.0.1', 5000)
