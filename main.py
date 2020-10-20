from flask import Flask, render_template
from flask_restful import Api, Resource
import beautifiul

app = Flask(__name__)
Api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class weather(Resource):
    def get(self):
        return beautifiul.scrape()


Api.add_resource(weather, '/api')
if __name__ == "__main__":
    app.run()
