import os
import json
import cherrypy
from jinja2 import Environment, FileSystemLoader
from cherrypy.lib.static import serve_file

class SiteGenerator:
    def __init__(self, template_dir='templates'):
        self.template_env = Environment(loader=FileSystemLoader(template_dir))
        self.generated_html = None

    @cherrypy.expose
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
            <h1>Welcome to the Site Generator API</h1>
            <div>
                <form action="/generate_site" method="post" enctype="multipart/form-data">
                    <label for="template">Upload Template:</label>
                    <input type="file" name="template" required><br>
                    <label for="json_file">Upload JSON File:</label>
                    <input type="file" name="json_file" required><br>
                    <button type="submit">Generate Site</button>
                </form>
            </div>
        </body>
        </html>
        """

    @cherrypy.expose
    def generate_site(self, template, json_file):
        # Retrieve the uploaded files from CherryPy request object
        template_file = template.file
        json_file = json_file.file

        # Load variables from JSON file
        variables = json.load(json_file)

        # Load Jinja template
        template_content = template_file.read().decode('utf-8')
        template_obj = self.template_env.from_string(template_content)

        # Render the template with variables
        self.generated_html = template_obj.render(variables)

        # Check if the self.generated_html is not null
        if self.generated_html:
            return self.generated_html
        else:
            return "Error generating site."

    @cherrypy.expose
    def get_generated_site(self):
        if self.generated_html:
            return self.generated_html
        else:
            return "No site generated yet."

if __name__ == '__main__':
    # Set the path to the directory containing your Jinja template
    template_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

    # Configure CherryPy server
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.quickstart(SiteGenerator(template_directory))
