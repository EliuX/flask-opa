package logging

 
import data.administrators

default allow = false
 

allow {
    input.user = administrators[_]
}

allow {
  contains(input.content, administrators[_])    
}