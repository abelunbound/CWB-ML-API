import flask
import functions_framework

@functions_framework.http
def cwb_sum_test(request: flask.Request) -> flask.typing.ResponseReturnValue:
    if request.is_json:
        data = request.get_json()
        field1 = data.get('field1', 0)
        field2 = data.get('field2', 0)

        try:
            field1 = float(field1)
            field2 = float(field2)
        except ValueError:
            return flask.Response("Invalid input: fields must be numbers.", status=400)

        total = field1 + field2
        return flask.jsonify({'sum': total})
    else:
        return flask.Response("Request must be JSON.", status=400)
