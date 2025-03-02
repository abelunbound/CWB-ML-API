gcloud functions deploy cwb_sum_test \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point cwb_sum_test