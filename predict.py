import pandas as pd
import numpy as np
np.bool = np.bool_ # https://stackoverflow.com/questions/74893742/how-to-solve-attributeerror-module-numpy-has-no-attribute-bool

import importlib

import functions.database
importlib.reload(functions.database)

from functions.database import (
    get_column_name_and_datatype_dictionary, 
    prepare_sql_queries_and_values,
    insert_data_into_sql_data_base,
    retrieve_data_from_sql,
    add_metadata_columns
)

import functions.machinelearning
importlib.reload(functions.machinelearning)

from functions.machinelearning import (
    prep_data_for_deep_ar_model,
    create_model_and_train,
    generate_forecasts,
    inverse_transform_forecasts,
    get_forecast_data_frames,

)

import functions.ml_evaluation
importlib.reload(functions.ml_evaluation)

from functions.ml_evaluation import (
    get_evaluation_metrics, 
    get_combined_rmse,
    get_experiment_number,
    get_hyperparameters,
)

import functions.applicant_assessment_results
importlib.reload(functions.applicant_assessment_results)

from functions.applicant_assessment_results import (
    assess_affordability,
    get_overall_assessment,
)

import warnings
warnings.filterwarnings('ignore')


def run_prediction(applicant_id = '123456799', required_amount = 14000): 
    
    print(f"Starting run_prediction with applicant_id={applicant_id}, required_amount={required_amount}\n")
    print("[STARTED] Step 1: Data collection\n")

    # Step 1: Data collection - ideally this should retrieve data for specified applicant id
    data = retrieve_data_from_sql("fin_history")
    
    # Example threshold amount
    print("[COMPLETED] Step 1: Data collection\n")
    print("[STARTED] Step 2: Prepare data for DeepAR\n")

    # Step 2: Prepare data for DeepAR - 
    # - Split data 
    # - Prep dynamic features
    # - normalise where neccessary, 
    # - scale balance with appropriate scaler 
    # - convert to expected GluonTS format

    # Split data: use first 7 months for training, last month for validation
    split_idx = len(data) - 30  # Last 30 days as validation
    train_data = data.iloc[:split_idx]

    training_data, scaler = prep_data_for_deep_ar_model(train_data)
    print("[COMPLETED] Step 2: Prepare data for DeepAR\n")
    print("[STARTED] Step 3: Create and train model\n")

    # Step 3: Create and train model
    forecasting_model_for_validation = create_model_and_train(training_data)
    print("[COMPLETED] Step 3: Create and train model\n")
    print("[STARTED] Step 4: Generate forecasts")

    # Step 4: Generate forecasts
    validation_forecasts, validation_tss = generate_forecasts(forecasting_model_for_validation, training_data)
    print("[COMPLETED] Step 4: Generate forecasts\n")
    print("[STARTED] Step 5: Inverse transform forecasts\n")

    # Step 5: Inverse transform forecasts
    transformed_validation_forecast_values = inverse_transform_forecasts(validation_forecasts[0], scaler)
    print("[COMPLETED] Step 5: Inverse transform forecasts\n")
    print("[STARTED] Step 6: Get forecast data frames \n")

    # Step 6: Get forecast data frames
    (forecast_7days_validation_set, 
    forecast_14days_validation_set, 
    forecast_30days_validation_set
    ) = get_forecast_data_frames(transformed_validation_forecast_values, data)
    print("[COMPLETED] Step 6: Get forecast data frames \n")
    print("[STARTED] Step 7: Get evaluation metrics \n")

    # Step 7: Get evaluation metrics
    combined_rmse_df = get_combined_rmse(forecast_7days_validation_set, forecast_14days_validation_set, forecast_30days_validation_set)
    print("[COMPLETED] Step 7: Get evaluation metrics  \n")
    print("[STARTED] Step 8. Get hyperparameters for the experiment for reference \n")
    

    # Step 8. Get hyperparameters for the experiment for reference
    # Define the path to the lightning_logs directory
    logs_dir = "lightning_logs"

    # experiment_no
    experiment_no = get_experiment_number(logs_dir)

    hyperparameters_path = f'lightning_logs/version_{experiment_no}/hparams.yaml'
    experiment_id = f'exp_{experiment_no}'
    hyperparameters_df = get_hyperparameters(hyperparameters_path, experiment_id)
    print("[COMPLETED] Step 8. Get hyperparameters for the experiment for reference  \n")
    print("[STARTED] Step 9: Extract key metrics for assessment using transformed values \n")

    # Step 9: Extract key metrics for assessment using transformed values

    # Final balance predictions (use the last value of each transformed forecast array)
    final_median = transformed_validation_forecast_values['p50'][-1]
    final_p10 = transformed_validation_forecast_values['p10'][-1]
    final_p90 = transformed_validation_forecast_values['p90'][-1]


    # Extract actual final balance if available
    if len(data) > len(train_data):
        actual_final = data['balance'].iloc[-1]
        error = actual_final - final_p90
        
        # Check if actual falls within the prediction interval
        within_interval = final_p10 <= actual_final <= final_p90
    
    print("[COMPLETED] Step 9: Extract key metrics for assessment using transformed values  \n")
    print("[STARTED] Step 10: Get overall affordability assessment \n")

    # Step 10: Get overall affordability assessment
    affordability_assessment = assess_affordability(required_amount, final_p10, final_p90)
    print("[COMPLETED] Step 10: Get overall affordability assessment  \n")
    print("[STARTED] Step 11: Get overall assessment \n")

    # Overall assessment 
    # Step 11: Get overall assessment
    experiment_id = f'exp_{experiment_no}'

    overall_validation_forecast_assessment_df = get_overall_assessment(
        experiment_id,
        required_amount, 
        affordability_assessment, 
        train_data, 
        final_p10, 
        final_median, 
        final_p90, 
        actual_final,
        error, 
        within_interval,
        )
    print("[COMPLETED] Step 11: Get overall assessment \n")
    print("[STARTED] Step 12: Concatenate hyperparameters and overall validation assessment into a single dataframe \n")
    # Step 12: Concatenate hyperparameters and overall validation assessment into a single dataframe
    hyperparameters_and_overall_validation_assessment_df = pd.concat([hyperparameters_df, overall_validation_forecast_assessment_df], ignore_index=True)

    print("[COMPLETED] Step 12: Concatenate hyperparameters and overall validation assessment into a single dataframe \n")
    print("[STARTED] Step 13: Insert into database\n")

    # Step 13: Insert into database
    # insert in database 
    # ................MODIFY TO HAVE UNIQUE ID FOR EACH APPLICANT................
    #  1. Forecasts x 30 days 
    #  2. feature engineered data (actual balance including 7days rolling average)
    #  3. Converted to gbp
    #  3. Hyperparameters & overall validation assessment

    # Database tables 

    dbname='cwb-database',

    #  delete/DROP later
    'cwb_results' # old table for holding results

    ##### Active tables
    # Financial history 
    fin_history_table_name = 'fin_history'
    fin_history_enhanced_table_name = 'fin_history_enhanced' # Feature engineered data, applicant id, date, time etc

    # Applicant Assessment and Model Evaluation 
    cwb_combined_rmse_table_name = 'cwb_combined_rmse' # Combined results for validation and future set
    cwb_validation_assessment_table_name = 'cwb_validation_assessment' # Assessment and Hyperparameters for validation set
    # cwb_future_assessment_table_name = 'cwb_future_assessment' # Assessment and Hyperparameters for future set

    # Forecasts
    cwb_validation_forecasts_table_name = 'cwb_validation_forecasts' # 30 days forecast, date, actual balance
    # gbp_cwb_validation_forecasts_table_name = 'gbp_cwb_validation_forecasts' # 30 days forecast, date, actual balance
    # cwb_future_forecasts_table_name = 'cwb_future_forecasts'  # 30 days forecast, date
    # gbp_cwb_future_forecasts_table_name = 'gbp_cwb_future_forecasts'  # 30 days forecast, date


    # Insert into database

    # Add meta data to Financial history enhanced
    data_df = add_metadata_columns(data, applicant_id = applicant_id)

    # Add metadata columns to combined RMSE
    combined_rmse_df = add_metadata_columns(combined_rmse_df, applicant_id = applicant_id)

    # Add meta data to relevant dataframes 
    hyperparameters_and_overall_validation_assessment_df = add_metadata_columns(hyperparameters_and_overall_validation_assessment_df, applicant_id = applicant_id)

    # Add metadata columns to validation forecasts
    forecast_30days_validation_set_df = add_metadata_columns(forecast_30days_validation_set, applicant_id = applicant_id)


    # 1. Financial history enhanced
    cwb_fin_history_enhanced_dict = get_column_name_and_datatype_dictionary(data_df)
    cwb_fin_history_enhanced_sql_queries_and_values = prepare_sql_queries_and_values(cwb_fin_history_enhanced_dict, fin_history_enhanced_table_name, data_df)
    insert_data_into_sql_data_base(*cwb_fin_history_enhanced_sql_queries_and_values)

    # 2. Combined RMSE
    cwb_rmse_dict = get_column_name_and_datatype_dictionary(combined_rmse_df)
    cwb_rsme_sql_queries_and_values = prepare_sql_queries_and_values(cwb_rmse_dict, cwb_combined_rmse_table_name, combined_rmse_df)
    insert_data_into_sql_data_base(*cwb_rsme_sql_queries_and_values)

    # 3. Validation Assessment Results (and Hyperparameters)
    cwb_validation_results_dict = get_column_name_and_datatype_dictionary(hyperparameters_and_overall_validation_assessment_df)
    cwb_validation_results_sql_queries_and_values = prepare_sql_queries_and_values(cwb_validation_results_dict, cwb_validation_assessment_table_name, hyperparameters_and_overall_validation_assessment_df)
    insert_data_into_sql_data_base(*cwb_validation_results_sql_queries_and_values)

    # 4. Validation Forecasts
    cwb_validation_forecasts_dict = get_column_name_and_datatype_dictionary(forecast_30days_validation_set_df)
    cwb_validation_forecasts_sql_queries_and_values = prepare_sql_queries_and_values(cwb_validation_forecasts_dict, cwb_validation_forecasts_table_name, forecast_30days_validation_set_df)
    insert_data_into_sql_data_base(*cwb_validation_forecasts_sql_queries_and_values)








