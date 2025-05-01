data "archive_file" "layer_code" {
  type        = "zip"
  output_path = "${path.module}/../packages/layer/layer.zip"
  source_dir  = "${path.module}/../dependencies"
}

resource "aws_lambda_layer_version" "dependencies" {
  layer_name       = "dependencies-layer"
  filename         = "${path.module}/../packages/layer/layer.zip"
  source_code_hash = data.archive_file.layer_code.output_base64sha256
}