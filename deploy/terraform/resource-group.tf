resource "azurerm_resource_group" "ascarlat_learning" {
  name     = var.resource_group_name
  location = var.location

  lifecycle {
    prevent_destroy = true
  }
}