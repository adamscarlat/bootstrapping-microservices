terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.102.0"
    }
  }

  required_version = ">= 1.7.5"
}

provider "azurerm" {
  features {}
}
