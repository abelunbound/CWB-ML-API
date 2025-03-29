import flask
import functions_framework
import os
import sys

# Add the parent directory to sys.path to resolve imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the prediction functionality
from predict import run_prediction  # Assuming predict.py has this function


@functions_framework.http
def run_ml_model(request: flask.Request) -> flask.typing.ResponseReturnValue:
    if request.is_json:
        data = request.get_json()
        applicant_id = data.get('applicant_id')
        required_amount = data.get('required_amount')

        # Validate inputs
        if applicant_id is None or required_amount is None:
            return flask.Response("Missing required fields: applicant_id and required_amount", status=400)
        
        try:
            # Convert required_amount to float if needed
            required_amount = float(required_amount)
        except ValueError:
            return flask.Response("Invalid input: required_amount must be a number.", status=400)

        try:
            # Run the ML model prediction using predict.py
            # This function will handle the database insertion
            run_prediction(applicant_id=applicant_id, required_amount=required_amount)
            
            # Return success message
            return flask.jsonify({
                "status": "success",
                "message": "Assessment completed and added to database"
            })
        except Exception as e:
            # Handle any errors from the prediction model
            return flask.Response(f"Error running the ML model: {str(e)}", status=500)
    else:
        return flask.Response("Request must be JSON.", status=400)