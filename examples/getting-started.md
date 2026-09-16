# Getting Started

This guide walks through a typical Krutrim Cloud workflow using the Krutrim Client SDK.

By the end of this guide, you will know how to:

1. Authenticate with the SDK
2. Create a VPC
3. Create an SSH Key
4. Provision a Virtual Machine
5. Retrieve VM details
6. Connect to the VM using SSH
7. Perform VM operations

> For complete API documentation, see `api_examples.ipynb`.

---

# Prerequisites

- Python 3.8+
- Krutrim Cloud Account
- API Key / Access Token

Install the SDK:

```bash
pip install krutrim-client
```

---

# Step 1: Initialize the SDK Client

```python
import os
from krutrim_client import KrutrimClient

client = KrutrimClient()  # reads KRUTRIMCLIENT_API_KEY from the environment
```

It is recommended to store your API key in environment variables or a `.env` file rather than hardcoding it.

---

# Step 2: Create a VPC

Example:

```python
success_response = client.highlvlvpc.create_vpc(
    k_customer_id="k-customer-id",
    x_account_id="acc-1234567890",
)

print(success_response.task_id)
```

Save the generated VPC identifier for future operations.

For additional VPC examples, see:

```text
examples/highlvlvpc/
```

---

# Step 3: Create an SSH Key

Generate an SSH key pair locally.

## Linux / macOS

```bash
ssh-keygen -t rsa -b 4096 -C "krutrim-demo"
```

View public key:

```bash
cat ~/.ssh/id_rsa.pub
```

## Windows PowerShell

```powershell
ssh-keygen -t rsa -b 4096 -C "krutrim-demo"
```

View public key:

```powershell
Get-Content $env:USERPROFILE\.ssh\id_rsa.pub
```

Upload the public key using the SSH Key examples available in:

```text
examples/sshkey/
```

---

# Step 4: Create a Virtual Machine

Use the VM provisioning APIs described in:

```text
api_examples.ipynb
```

Typical inputs include:

- Image ID
- Flavor ID
- VPC ID
- SSH Key ID

Store the returned VM identifier.

---

# Step 5: Retrieve VM Details

Retrieve VM information to obtain details such as:

- VM Status
- Public IP Address
- Network Configuration

Refer to:

```text
api_examples.ipynb
```

for complete examples.

---

# Step 6: Connect to the VM

After the VM becomes active and a public IP is assigned, connect using SSH.

## Linux / macOS

```bash
ssh -i ~/.ssh/id_rsa ubuntu@<PUBLIC_IP>
```

## Windows PowerShell

```powershell
ssh -i $env:USERPROFILE\.ssh\id_rsa ubuntu@<PUBLIC_IP>
```

Replace:

```text
<PUBLIC_IP>
```

with your VM's public IP address.

---

# Common Usernames

| Operating System | Username |
|------------------|----------|
| Ubuntu | ubuntu |
| Debian | debian |
| CentOS | centos |
| Rocky Linux | rocky |
| AlmaLinux | almalinux |

---

# Step 7: Manage the VM

Common lifecycle operations include:

- Start
- Stop
- Reboot
- Delete

Examples are available in:

```text
examples/startStopVM/
```

---

# Troubleshooting

## Authentication Errors

Verify:

- API key is valid
- Environment variable is configured correctly
- Account has required permissions

---

## Permission denied (publickey)

Verify:

- Correct SSH key was uploaded
- Correct private key is being used
- VM is running
- Security group allows SSH access

---

## Connection timed out

Verify:

- VM is in ACTIVE state
- Public IP is assigned
- Port 22 is open

---

# Additional Resources

| Resource | Location |
|-----------|----------|
| Full API Documentation | `api_examples.ipynb` |
| VPC Examples | `examples/highlvlvpc/` |
| SSH Key Examples | `examples/sshkey/` |
| Security Group Examples | `examples/securityGroup/` |
| VM Operations | `examples/startStopVM/` |

For detailed API usage and advanced options, refer to `api_examples.ipynb`.
