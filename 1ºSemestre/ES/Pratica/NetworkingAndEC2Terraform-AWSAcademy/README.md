
# README

## Running

```bash
export TF_VAR_aws_access_key_id="<aws_access_key_id>"
export TF_VAR_aws_access_key_secret="<aws_access_key_secret>"
export TF_VAR_aws_session_token="<aws_session_token>"

terraform plan -var="ssh_key_pub_location=ssh-keys/ec2-key.pub"
terraform apply -var="ssh_key_pub_location=ssh-keys/ec2-key.pub"
terraform destroy

```