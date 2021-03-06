import base64
import os
import datetime
from urllib.parse import quote as urlquote
from shutil import copyfile
from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


UPLOAD_DIRECTORY = "/project/app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


app.layout = html.Div(
    [
        html.H1("CSV Insight"),
        html.H2("Upload CSV file"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,
        ),
        html.H1(id="file-list"),
        html.H2("Upload config (yaml) file"),
        dcc.Upload(
            id="upload-config",
            children=html.Div(
                ["Drag and drop or click to select a configuration (yaml) file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False,
        ),
        #html.H2("File List"),
        #html.Ul(id="file-list"),
        html.H1(id="file-config"),
    ],
    style={"max-width": "500px"},
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb+") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    # for filename in os.listdir(UPLOAD_DIRECTORY):
    #     path = os.path.join(UPLOAD_DIRECTORY, filename)
    #     if os.path.isfile(path):
    #         files.append(filename)
    files.append("charting.csv")
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    #print("location: ", location)
    #return html.A(filename, href=location)
    #os.system('python cli.py "..\..\Additional files\Sacramentorealestatetransactions.csv" --chart --dialect delimiter=,')
    #os.system('python cli.py location --chart --dialect delimiter=,')
    #return html.A(filename, href="http:127.0.0.1:8050",target='_blank')

    #urlforDash = "http://127.0.0.1:8050?"+"filename=" + filename
    urlForDash = "http://127.0.0.1:8050"
    return html.Div([html.A("Click to chart: " + filename , href=urlForDash, target='_blank')])
    #return html.A(filename, href=location)


@app.callback(
    Output("file-config", "children"),
    [Input("upload-config", "filename"), Input("upload-config", "contents")],
)
def update_config(uploaded_filename, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filename is not None and uploaded_file_contents is not None:
        #save_file(uploaded_filename, uploaded_file_contents)
        save_file("config.yaml", uploaded_file_contents)
        return[html.P("Configuration file used: " + uploaded_filename)] # to display uploaded config file

@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filename, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filename is not None and uploaded_file_contents is not None:
        #save_file(uploaded_filename, uploaded_file_contents)
        save_file("charting.csv", uploaded_file_contents)
        return[html.Li(file_download_link(uploaded_filename))] # to display uploaded data file

    # files = uploaded_files()
    # if len(files) == 0:
    #     return [html.Li("No files yet!")]
    # else:
    #     return [html.Li(file_download_link(filename)) for filename in files]




if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
