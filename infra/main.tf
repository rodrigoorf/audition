terraform {
    required_providers {
      azurerm = {
        source = "hashicorp/azurerm"
        version = "~> 3.47.0"
      }
    }

    required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name = "Rg-aks-resource-group"
  location = "southcentralus"
}

resource "azurerm_kubernetes_cluster" "aks" {
  name = "rodrigok8s"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix = "rodrigok8s"

  default_node_pool {
    name = "default"
    node_count = 1
    vm_size = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Sandbox"
  }
}

resource "azurerm_container_registry" "acr" {
  name = "rodrigofreacr"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  sku = "Standard"
  admin_enabled = false
}

resource "azurerm_role_assignment" "acr_aks" {
  principal_id = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name = "AcrPull"
  scope = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}