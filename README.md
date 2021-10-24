# counter-reset

This project contains source code and supporting files for a serverless application to build & deploy with the SAM CLI & GitHub Actions. It includes the following files and folders

- counter_reset - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Deployment for application

The application is automated for deployment

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
counter-reset$ sam build --use-container
```

Application dependencies are defined in `counter_reset/requirements.txt`

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.