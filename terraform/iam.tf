## ROLE POLICY FOR THE LAMBDA

data "aws_iam_policy_document" "lambda_trust_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust_policy.json
}



## POLICY TO SEND TO QUEUE 

data "aws_iam_policy_document" "lambda_sqs_policy" {
  statement {
    resources = ["${aws_sqs_queue.terraform_queue.arn}"]
    actions   = ["sqs:GetQueueUrl", "sqs:SendMessage"]
  }
}

resource "aws_iam_policy" "lambda_sqs" {
  name   = "lambda-sqs"
  policy = data.aws_iam_policy_document.lambda_sqs_policy.json
}

resource "aws_iam_policy_attachment" "lambda_sqs_policy_attachment" {
  name       = "attach-lambda-sqs-policy"
  roles      = [aws_iam_role.lambda_role.name]
  policy_arn = aws_iam_policy.lambda_sqs.arn
}