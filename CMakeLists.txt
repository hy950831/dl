               
# @TAG(DATA61_BSD)    
cmake_minimum_required(VERSION 3.7.2)
# declare the dl CMake project and the languages it is written in (just C)
project(dl C)                                                                              
# Name the executable and list source files required to build it
add_executable(dl src/main.c)
                             
# List of libraries to link with the application.
target_link_libraries(dl
    sel4                     
    muslc utils
    sel4muslcsys sel4utils)
                             
# Tell the build system that this application is the root task.
DeclareRootserver(dl)