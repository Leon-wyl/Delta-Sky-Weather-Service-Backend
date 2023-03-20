# This is the lambda function itself, which is sourced from NewRelic's official GitHub
module "newrelic_log_ingestion" {
  source             = "github.com/newrelic/aws-log-ingestion"
  nr_license_key     = "{{b43497e898fe8785a353d22f8125c7fd39cdNRAL}}"
  nr_tags = "NR function"
  service_name = "${var.group_name}_${terraform.workspace}_newrelic_log_ingestion"
  nr_logging_enabled = true
  build_lambda = true
}

# This resource configures when the lambda function is triggered
resource "aws_cloudwatch_event_rule" "newrelic_log_ingestion" {
  name                = "${var.group_name}_${terraform.workspace}_newrelic_log_ingestion"
  description         = "Schedule for NewRelic Log-Ingestion Lambda Function"            
  schedule_expression = "rate(5 minutes)"                              
}

resource "aws_cloudwatch_event_target" "newrelic_log_ingestion" {
  rule      = aws_cloudwatch_event_rule.newrelic_log_ingestion.name
  target_id = "${var.group_name}_${terraform.workspace}_scheduled" # TODO: change here
  arn       = aws_lambda_function.newrelic_log_ingestion.arn                         # TODO: change here
}

# Allows your function to be invoked by the Event Bridge.
resource "aws_lambda_permission" "newrelic_log_ingestion" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.newrelic_log_ingestion.function_name # TODO: change here
  principal     = "events.amazonaws.com"
}

# Including this resource will keep a log as your function being called
resource "aws_cloudwatch_log_group" "newrelic_log_ingestion_log" {
  name              = "/aws/lambda/${aws_lambda_function.newrelic_log_ingestion.function_name}" # TODO: change here
  retention_in_days = 7
  lifecycle {
    prevent_destroy = false
  }
}
