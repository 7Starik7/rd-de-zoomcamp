##### Refresh service-account's auth-token for this session
```
gcloud auth application-default login
```
##### Initialize state file (.tfstate) - should be executed in terraform directory
```
terraform init
```
##### Check changes to new infra plan
```
terraform plan
```
##### Create new infra
```
terraform apply
```
##### Delete infra after your work, to avoid costs on any running services
```
terraform destroy
```