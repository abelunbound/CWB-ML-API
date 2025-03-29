import flask
import functions_framework

@functions_framework.http
def run_ml_model(request):
    return flask.jsonify({"status": "success", "message": "Function is working"})