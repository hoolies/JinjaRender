"""This script will render a Jinja Template with a Json file"""
"""This script is made by xrouvell in order to test Jinja2 templates with CherryPy (like SoL)"""
from cherrypy import config, expose, quickstart
from json import loads
from jinja2 import Environment

class SiteGenerator:
    def __init__(self):
        self.template_env = Environment() 
        self.generated_html = None
        self.cherrypy_config = config.update({
            'server.socket_host': '0.0.0.0',                # Keep in mind 0.0.0.0 allows everyone even public IP, use 127.0.0.0/8 if you want local
            'server.socket_port': 44380,                    # Feel free to change the port
            'server.thread_pool': 8,                        # How many concurrent connection you support
            'server.protocol_version': 'HTTP/1.1',
            'server.ssl_module':'builtin',                  # If we want to host it in the future we can have an ssl certificate
            })


    @expose
    def index(self):
        return """
        <html>
            <style>
                input[type=file], select {
                  width: 100%;
                  padding: 12px 20px;
                  margin: 8px 0;
                  display: inline-block;
                  border: 1px solid #ccc;
                  border-radius: 4px;
                  box-sizing: border-box;
                }

                input[type=submit] {
                  width: 100%;
                  color: white;
                  padding: 14px 20px;
                  margin: 8px 0;
                  border: none;
                  border-radius: 4px;
                }

                input[type=submit]:hover {
                }

                div {
                  border-radius: 5px;
                  background-color: #f2f2f2;
                  padding: 20px;
                }
            </style>
            <body>
                <h1>Jinja Renderer</h1>
                <div>
                    <form action="/generate_site">
                        <label for="template">Jinja Template:</label><br>
                        <textarea id="template" name="template" placeholder="Paste your template here..." rows="4" cols="50"></textarea><br><br>
                        <label for="json_file">JSON File:</label><br>
                        <textarea id="json_file" name="json_file" placeholder="Paste your JSON here..." rows="4" cols="50"></textarea><br><br>
                        <button type="submit">Generate Site</button><br>
                    </form>
                </div>
            </body>
        </html>
        """

    @expose
    def generate_site(self, template, json_file):
      try:
        # Check if the JSON file is valid
        json_data = loads(json_file)
        # Check if Jinja template is valid
        template = self.template_env.from_string(template)
        # Render the template with the JSON data
        self.generated_html = template.render(json_data)

        # Genereates the site
        return self.generated_html

      except Exception as e:
        return f"Error: {e}"


def main():
    # Quick loads the site through the Class
    quickstart(SiteGenerator())


if __name__ == '__main__':
    main()
