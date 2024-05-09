resource "azurerm_container_registry" "container_registry" {
  name                = var.app_name
  location            = var.location
  resource_group_name = azurerm_resource_group.ascarlat_learning.name

  admin_enabled = true
  sku           = "Basic"

  lifecycle {
    prevent_destroy = true
  }
}