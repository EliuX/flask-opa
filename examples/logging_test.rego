package logging

test_default_denied {
    not allow
}

test_admin_user_allowed {
    allow with input as {"user": "eliux"}
    allow with input as {"user": "jon", "content": "..."}
}

test_non_admin_users_denied { 
    not allow with input as {"user": ""}
    not allow with input as {"user": "george"}
}

test_content_related_to_admin_allowed {  
    allow with input as {"user": "anyone", "content": "requested help to eliux"}
    allow with input as {"user": "anyone", "content": "requested help to jon snow"}
}

test_content_non_related_to_admin_denied {  
    not allow with input as {"user": "anyone"}
    not allow with input as {"user": "anyone", "content": ""}
    not allow with input as {"user": "anyone", "content": "lorem ipsum dolor"}
}