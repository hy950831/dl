
#
# Copyright 2018, Data61
# Commonwealth Scientific and Industrial Research Organisation (CSIRO)
# ABN 41 687 119 230.
#
# This software may be distributed and modified according to the terms of
# the BSD 2-Clause license. Note that NO WARRANTY is provided.
# See "LICENSE_BSD2.txt" for details.
#
# @TAG(DATA61_BSD)
#
ImportCapDL()
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -u __vsyscall_ptr")


# FIXME: should I add the shared lib in cdl_pp?
# or how should i modify the cdl_pp function?
cdl_pp(${CMAKE_CURRENT_SOURCE_DIR}/manifest.py cdl_pp_target
    ELF "program_1"
    CFILE "${CMAKE_CURRENT_BINARY_DIR}/cspace_program_1.c"

    ELF "program_2"
    CFILE "${CMAKE_CURRENT_BINARY_DIR}/cspace_program_2.c"

    # FIXME: go understand the cdl_pp process
    # NOTE: currently the cdl_pp processing will create a symbol declearation
    # file which depends on sel4 and other libraries. which are statically
    # compiled, hence i need to modify cdl_pp(func manifest in capdl_linker.py)
    # somehow to correctly process shared libs

    # ELF "shared_lib"
    # CFILE "${CMAKE_CURRENT_BINARY_DIR}/cspace_lib.c"
)

add_executable(program_1 EXCLUDE_FROM_ALL program_1.c cspace_program_1.c)

# FIXME: include directory doesn't work?
target_include_directories(program_1 PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")

add_dependencies(program_1 cdl_pp_target)
target_link_libraries(program_1 sel4tutorials)

list(APPEND elf_files "$<TARGET_FILE:program_1>")
list(APPEND elf_targets "program_1")

# Try to compile the shared library
# FIXME: compile a duplicate set of sel4 kernel with -fPIC ????
SET_PROPERTY(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)
add_library(shared_lib SHARED lib/set.c)

# FIXME: modify capdl_loader.py to somehow support shared objects in
# the elf list
# list(APPEND elf_files "$<TARGET_FILE:shared_lib>")
# list(APPEND elf_targets "shared_lib")

add_executable(program_2 EXCLUDE_FROM_ALL program_2.c cspace_program_2.c)
add_dependencies(program_2 cdl_pp_target)
# target_include_directories(program_2 PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")
target_link_libraries(program_2 sel4tutorials)

list(APPEND elf_files "$<TARGET_FILE:program_2>")
list(APPEND elf_targets "program_2")

cdl_ld("${CMAKE_CURRENT_BINARY_DIR}/spec.cdl" capdl_spec
    MANIFESTS ${CMAKE_CURRENT_SOURCE_DIR}/manifest.py
    ELF ${elf_files}
    DEPENDS ${elf_targets})

DeclareCDLRootImage("${CMAKE_CURRENT_BINARY_DIR}/spec.cdl" capdl_spec ELF ${elf_files} ELF_DEPENDS ${elf_targets})


set(FINISH_COMPLETION_TEXT "lazy")
set(START_COMPLETION_TEXT "
the
the
the")
configure_file(${CMAKE_SOURCE_DIR}/projects/sel4-tutorials/tools/expect.py ${CMAKE_BINARY_DIR}/check @ONLY)
