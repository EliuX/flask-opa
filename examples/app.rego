package examples

import data.administrators

default allow = false
 
allow {
    input.method = "GET" 
    input.path = []
}

allow {
    input.method = "GET" 
    input.path = ["list"]
    is_administrator
}

allow {
    input.method = "GET"
    its_own_data
}

allow {
    input.method = "GET"
    input.path = ["data", _]
    is_administrator
}

allow {
    input.method = "POST"
    its_own_data
}

allow {
    input.method = "POST"
    input.path = ["data", _]
    is_administrator
}

allow {
    input.method = "DELETE"
    input.path = ["data", _]
    is_administrator
}

pii = ["ssn"] {
    not its_own_data
    not is_administrator
}

its_own_data { 
    input.path = ["data", user_id]
    input.user = user_id
}

is_administrator {
    input.user = administrators[_]
}
