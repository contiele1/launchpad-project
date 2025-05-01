resource "aws_lambda_function" "call_lambda" {
    filename         = "${path.module}/../packages/call/function.zip"
    function_name    = var.call_lambda_name
    role             = aws_iam_role.call_lambda_role.arn
    handler          = "call_api.call_lambda_handler"
    source_code_hash = filebase64sha256("${path.module}/../src/call_api.py")
    runtime          = "python3.9"
    layers = [aws_lambda_layer_version.dependencies.arn]
}

data "archive_file" "lambda" {
    type        = "zip"
    source_file      = "${path.module}/../src/call_api.py"
    output_path      = "${path.module}/../packages/call/function.zip"
}
