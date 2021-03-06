
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

# include(helper.cmake)

# XXX: should I add the shared lib in cdl_pp?
# or how should i modify the cdl_pp function?
cdl_pp(${CMAKE_CURRENT_SOURCE_DIR}/manifest.py cdl_pp_target
    ELF "program_1"
    CFILE "${CMAKE_CURRENT_BINARY_DIR}/cspace_program_1.c"

    ELF "program_2"
    CFILE "${CMAKE_CURRENT_BINARY_DIR}/cspace_program_2.c"
)

add_executable(program_1 EXCLUDE_FROM_ALL program_1.c cspace_program_1.c)
# this cdl_pp_target is the generated cspace_program_*.c
# make sure the cdl_pp_target is generated before program_1
add_dependencies(program_1 cdl_pp_target)
# add_dependencies(program_1 cdl_pp_target sel4platsupport sel4muslcsys muslc sel4)

target_include_directories(program_1 PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")
target_link_libraries(program_1 sel4tutorials)

# add the result file of program_1 to the elf_files list
list(APPEND elf_files "$<TARGET_FILE:program_1>")
list(APPEND cpio_files "$<TARGET_FILE:program_1>")

# add program_1 to target list
list(APPEND elf_targets "program_1")

SET_PROPERTY(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)
add_library(shared SHARED lib/set.c )
target_compile_options(
    shared PRIVATE
    -fPIC -nostdlib
    )

# NOTE: modify capdl_loader.py to somehow support shared objects in
# the elf list
list(APPEND cpio_files "$<TARGET_FILE:shared>")
list(APPEND so_files "$<TARGET_FILE:shared>")
list(APPEND elf_targets "shared")

add_executable(program_2 EXCLUDE_FROM_ALL program_2.c cspace_program_2.c)
add_dependencies(program_2 cdl_pp_target)
target_include_directories(program_2 PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")
target_link_libraries(program_2 sel4tutorials)

list(APPEND elf_files "$<TARGET_FILE:program_2>")
list(APPEND cpio_files "$<TARGET_FILE:program_2>")
list(APPEND elf_targets "program_2")

cdl_ld_with_so("${CMAKE_CURRENT_BINARY_DIR}/spec.cdl" capdl_spec
    MANIFESTS ${CMAKE_CURRENT_SOURCE_DIR}/manifest.py
    ELF ${elf_files}
    SO ${so_files}
    DEPENDS ${elf_targets}
    )

# Here we need another copy of program_2 binary named as program_2_data which is used to
# calculate the relocation. since the final program_2 will depend on the relocation file
# and the program_2 binary is used to generate the relocation file which will form a strong
# circular dependency, hence another copy should be necessary
add_executable(program_2_data EXCLUDE_FROM_ALL program_2.c cspace_program_2.c)
add_dependencies(program_2_data cdl_pp_target)
target_include_directories(program_2_data PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")
target_link_libraries(program_2_data sel4tutorials)
target_link_libraries(program_2_data -Wl,-Bdynamic shared)

add_executable(program_1_data EXCLUDE_FROM_ALL program_1.c cspace_program_1.c)
add_dependencies(program_1_data cdl_pp_target)
target_include_directories(program_1_data PUBLIC "${CMAKE_CURRENT_LIST_DIR}/include")
target_link_libraries(program_1_data sel4tutorials)
target_link_libraries(program_1_data -Wl,-Bdynamic shared)

cdl_calc_relo($<TARGET_FILE:program_1_data> $<TARGET_FILE:shared> program_1_symbolfile symbolfile_tar_1)
cdl_calc_relo($<TARGET_FILE:program_2_data> $<TARGET_FILE:shared> program_2_symbolfile symbolfile_tar_2)

add_dependencies(symbolfile_tar_2 program_2_data)
add_dependencies(program_2 symbolfile_tar_2)

add_dependencies(symbolfile_tar_1 program_1_data)
add_dependencies(program_1 symbolfile_tar_1)

target_link_libraries(program_2
    -Wl,--just-symbols=${CMAKE_CURRENT_BINARY_DIR}/program_2_symbolfile
    -Wl,-Bdynamic shared
    )

target_link_libraries(program_1
    -Wl,--just-symbols=${CMAKE_CURRENT_BINARY_DIR}/program_1_symbolfile
    -Wl,-Bdynamic shared
    )

DeclareCDLRootImageDyn("${CMAKE_CURRENT_BINARY_DIR}/spec.cdl" capdl_spec ELF ${cpio_files} ELF_DEPENDS ${elf_targets})

configure_file(${CMAKE_SOURCE_DIR}/projects/sel4-tutorials/tools/expect.py ${CMAKE_BINARY_DIR}/check @ONLY)
