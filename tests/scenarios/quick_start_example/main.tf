variable "my_var" {}

resource "random_string" "this" {
  length = 6
}

output "example_name" {
  value = "quick-start"
}

output "random_string" {
  value = random_string.this.result
}

output "my_var" {
  value = var.my_var
}