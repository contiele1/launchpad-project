data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/../src/main.py"
  output_path = "${path.module}/../packages/function.zip"
}

resource "aws_lambda_function" "lambda" {
  filename         = "${path.module}/../packages/function.zip"
  function_name    = var.lambda_name
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/../src/main.py")
  runtime          = "python3.9"
  layers           = [aws_lambda_layer_version.dependencies.arn]
}

