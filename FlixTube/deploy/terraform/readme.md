Ignoring a resource on destroy
------------------------------
* When destroying the infrastructure, we can keep some of the resources we don't want destroyed.

* Remove the resource from the state:

```bash
terraform state rm azurerm_resource_group.ascarlat_learning
```

* Run terraform destroy
  - The resource will get skipped

* Next time you're ready to run terraform apply, import the resource back to the state prior to the apply:
  - Syntax is `terraform import <tf_resource_name> <resource_actual_id>
  
```bash
terraform import azurerm_resource_group.ascarlat_learning /subscriptions/b1727ba9-866b-4deb-af19-afeaa4644c88/resourceGroups/ascarlat_learning

terraform apply
```