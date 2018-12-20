
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

include(helper.cmake)


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
)


add_executable(program_1 EXCLUDE_FROM_ALL program_1.c cspace_program_1.c)
# this cdl_pp_target is the generated cspace_program_*.c
# make sure the cdl_pp_target is generated before program_1
add_dependencies(program_1 cdl_pp_target)
# add_dependencies(program_1 cdl_pp_target sel4platsupport sel4muslcsys muslc sel4)

# FIXME: include directory doesn't work?
target_include_directories(program_1 PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")

# staticlly link the program_1 with the tutorial lib which is already
# linked with sel4 muslc and etc
target_link_libraries(program_1 sel4tutorials)

# FIXME: linking with the libs below won't set up the serial even explicitly called
# the serial setup function
# target_link_libraries( program_1 Configuration sel4platsupport sel4muslcsys muslc sel4)


# TODO: add a helper function to manually set so dependencies
# declare_so_dependency(program_1 shared)

# add the result file of program_1 to the elf_files list
list(APPEND elf_files "$<TARGET_FILE:program_1>")
list(APPEND cpio_files "$<TARGET_FILE:program_1>")
# add program_1 to target list
list(APPEND elf_targets "program_1")

# Try to compile the shared library
# FIXME: compile a duplicate set of sel4 kernel with -fPIC ????
SET_PROPERTY(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)
add_library(shared SHARED lib/set.c)


# FIXME: modify capdl_loader.py to somehow support shared objects in
# the elf list
list(APPEND cpio_files "$<TARGET_FILE:shared>")

list(APPEND so_files "$<TARGET_FILE:shared>")
list(APPEND elf_targets "shared")

add_executable(program_2 EXCLUDE_FROM_ALL program_2.c cspace_program_2.c)
# add_dependencies(program_2 Configuration cdl_pp_target sel4platsupport sel4muslcsys muslc sel4)
add_dependencies(program_2 cdl_pp_target)
# target_include_directories(program_2 PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")
target_link_libraries(program_2 sel4tutorials)
# target_link_libraries( program_2 Configuration sel4platsupport sel4muslcsys muslc sel4)

list(APPEND elf_files "$<TARGET_FILE:program_2>")
list(APPEND cpio_files "$<TARGET_FILE:program_2>")
list(APPEND elf_targets "program_2")

cdl_ld_with_so("${CMAKE_CURRENT_BINARY_DIR}/spec.cdl" capdl_spec
    MANIFESTS ${CMAKE_CURRENT_SOURCE_DIR}/manifest.py
    ELF ${elf_files}
    SO ${so_files}
    DEPENDS ${elf_targets}
    )


DeclareCDLRootImage("${CMAKE_CURRENT_BINARY_DIR}/spec.cdl" capdl_spec ELF ${cpio_files} ELF_DEPENDS ${elf_targets})


set(FINISH_COMPLETION_TEXT "lazy")
set(START_COMPLETION_TEXT "
the
the
the")
configure_file(${CMAKE_SOURCE_DIR}/projects/sel4-tutorials/tools/expect.py ${CMAKE_BINARY_DIR}/check @ONLY)
