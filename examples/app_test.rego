package examples

test_by_default_not_allowed {
    not allow
}

test_home_allowed {
    allow with input as {"method":"GET","path":[]}
    allow with input as {"method":"GET","path":[],"user":"invaliduser"}
}

test_get_list__using_non_admin_user_denied { 
   not allow with input as {"method":"GET","path":["list"]}
   not allow with input as {"method":"GET","path":["list"], "user":""}
   not allow with input as {"method":"GET","path":["list"], "user":"anyone"}
}

test_get_list__using_admin_user_allowed {  
   allow with input as {"method":"GET","path":["list"], "user":"eliux"}
   allow with input as {"method":"GET","path":["list"], "user":"jon"}
}

test_get_data__using_non_admin_user_denied {
   not allow with input as {"method":"GET","path":["data"]}
   not allow with input as {"method":"GET","path":["data","anyone"], "user":""}
   not allow with input as {"method":"GET","path":["data","eliux"], "user":"anyone"}
}

test_get_data__using_admin_user_allowed { 
   allow with input as {"method":"GET","path":["data","anyone"], "user":"eliux"}
   allow with input as {"method":"GET","path":["data","anyone"], "user":"jon"}
}

test_get_its_own_data_allowed {
   allow with input as {"method":"GET","path":["data","eliux"], "user":"eliux"}
   allow with input as {"method":"GET","path":["data","anyone"], "user":"anyone"}
}

test_post_user_data_using_non_admin_user_denied {
   not allow with input as {"method":"POST","path":["data","eliux"], "user":""}
   not allow with input as {"method":"POST","path":["data","jon"], "user":"anyone"}
}

test_post_user_data_using_admin_user_allowed {
   allow with input as {"method":"POST","path":["data","anyone"], "user":"eliux"}
   allow with input as {"method":"POST","path":["data","eliux"], "user":"jon"}
}

test_post_its_own_data_allowed {
   allow with input as {"method":"POST","path":["data","eliux"], "user":"eliux"}
   allow with input as {"method":"POST","path":["data","anyone"], "user":"anyone"}
}

test_delete_using_non_admin_user_denied {
   not allow with input as {"method":"DELETE","path":["data","anyone"], "user":""}
   not allow with input as {"method":"DELETE","path":["data","eliux"], "user":"anyone"}
}

test_delete_using_admin_user_allowed {
   allow with input as {"method":"DELETE","path":["data","anyone"], "user":"eliux"}
   allow with input as {"method":"DELETE","path":["data","eliux"], "user":"jon"}
}

test_pii_non_admin_user_get_another_user_user {
    pii = ["ssn"] with input as {"method":"GET","path":["data","user1"], "user":"user2"} 
}