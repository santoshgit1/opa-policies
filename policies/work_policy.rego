package workpolicy

# Define a default policy
default allow = false

# Admins are always allowed
allow {
    input.user.role == "admin"
}

# Engineers are allowed read access
allow {
    input.user.role == "engineer"
    input.action == "read"
}
