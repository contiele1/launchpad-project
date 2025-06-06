resource "aws_sqs_queue" "terraform_queue" {
  name                      = var.sqs_name
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 259200
  receive_wait_time_seconds = 0
}