# Deployment Guide for Weather Time App

## Prerequisites

-   Google Cloud SDK installed and authenticated
-   `gcloud` CLI configured
-   `adk` CLI installed
-   A valid **GOOGLE_API_KEY** environment variable exported


------------------------------------------------------------------------

## 0. Prerequisites - Verification

``` bash
echo ${GOOGLE_API_KEY: -5}              # Verify google API Key

PROJECT_ID=ENTER_PROJECT_ID_HERE
GCP_USER=ENTER_GCP_USER_OR_EMAIL_HERE



gcloud config set project $PROJECT_ID   # Set active project
gcloud config get project   # Verify active project

# Enable secrets manager for the acitve project
gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID


```

------------------------------------------------------------------------

## 1. Create a Secret in Google Secret Manager

``` bash
echo $GOOGLE_API_KEY | gcloud secrets create GOOGLE_API_KEY --project=$PROJECT_ID --data-file=-
```

------------------------------------------------------------------------

## 2. Grant Access to the Compute Service Account

``` bash

# List Service Account
gcloud iam service-accounts list

# Create Service Account
gcloud iam service-accounts create my-adk-service-account \
        --description="Service account for my AI Agent" \
        --display-name="ADK Agent Service Account"

# Bind Service Account
gcloud projects add-iam-policy-binding $PROJECT_ID     \
    --member="serviceAccount:my-adk-service-account@$PROJECT_ID.iam.gserviceaccount.com"  \
    --role="roles/secretmanager.secretAccessor"



# 1. Grant permission to build and deploy Cloud Run services
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:my-adk-service-account@$PROJECT_ID.iam.gserviceaccount.com"  \
    --role="roles/run.builder"

# 2. Grant permission to access the source code bucket
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:my-adk-service-account@$PROJECT_ID.iam.gserviceaccount.com"  \
    --role="roles/storage.objectViewer"

# 3. Grant the Service Account User role (required to "act as" the account)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:my-adk-service-account@$PROJECT_ID.iam.gserviceaccount.com"  \
    --role="roles/iam.serviceAccountUser"



# PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
#     --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
#     --role="roles/secretmanager.secretAccessor" \
#     --project="$PROJECT_ID"


# gcloud secrets add-iam-policy-binding GOOGLE_API_KEY --member="COMPUTE_SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor" --project="${PROJECT_ID}"
```

------------------------------------------------------------------------

## 3. Set Required Environment Variables

``` bash
export GOOGLE_CLOUD_PROJECT="${PROJECT_ID}"
export GOOGLE_CLOUD_LOCATION="us-central1"
export AGENT_PATH="./greeting_agent"
export SERVICE_NAME="weather-time"
export APP_NAME="weather_time_app"
```

------------------------------------------------------------------------

## 4. Deploy to Cloud Run Using ADK

``` bash
adk deploy cloud_run --project=$GOOGLE_CLOUD_PROJECT --region=$GOOGLE_CLOUD_LOCATION --service_name=$SERVICE_NAME --app_name=$APP_NAME --with_ui $AGENT_PATH
```

------------------------------------------------------------------------

## Notes

-   Ensure that the Agent Path (`./greeting_agent`) contains the required
    ADK agent files.
-   The `--with_ui` flag deploys the UI alongside the Cloud Run service.
-   Replace identifiers with your actual project details if deploying in
    a different environment.

------------------------------------------------------------------------

## Troubleshooting

-   Verify Secret Manager permissions if deployment fails to access
    `GOOGLE_API_KEY`
-   Ensure Cloud Run API is enabled:

``` bash
gcloud services enable run.googleapis.com
```