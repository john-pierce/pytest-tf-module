variable "pass_through" {}

module "quick_start" {
  source = "../.."

  my_var = var.pass_through
}

output "example_name" {
  value = module.quick_start.example_name
}

output "random_string" {
  value = module.quick_start.random_string
}

output "pass_through" {
  value = module.quick_start.my_var
}