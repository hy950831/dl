function(cdl_ld_with_so outfile output_target)
    cmake_parse_arguments(PARSE_ARGV 2 CDL_LD "" "" "ELF;MANIFESTS;DEPENDS;SO")
    if (NOT "${CDL_LD_UNPARSED_ARGUMENTS}" STREQUAL "")
        message(FATAL_ERROR "Unknown arguments to cdl_ld_with_so")
    endif()

    add_custom_command(OUTPUT "${outfile}"
        COMMAND ${python_with_capdl} ${CDL_LD_MANIFESTS} |
        ${capdl_linker_tool}
            --arch=${KernelSel4Arch}
            gen_cdl
            --manifest-in -
            --elffile ${CDL_LD_ELF}
            --sofile ${CDL_LD_SO}
            --outfile ${outfile}
        DEPENDS ${CDL_LD_ELF} ${capdl_python} ${CDL_LD_MANIFESTS})
    add_custom_target(${output_target}
        DEPENDS "${outfile}")
    add_dependencies(${output_target} ${CDL_LD_DEPENDS})
endfunction()

function(cdl_pp_with_so manifest_in target target_so)
    cmake_parse_arguments(PARSE_ARGV 3 CDL_PP "" "" "ELF;CFILE;DEPENDS;SO;SO_CFILE")
    if (NOT "${CDL_PP_UNPARSED_ARGUMENTS}" STREQUAL "")
        message(FATAL_ERROR "${CDL_PP_UNPARSED_ARGUMENTS}")
        message(FATAL_ERROR "Unknown arguments to cdl_pp_with_so")
    endif()

    add_custom_command(OUTPUT ${CDL_PP_CFILE}
        COMMAND ${python_with_capdl} ${manifest_in} |
        ${capdl_linker_tool}
                --arch=${KernelSel4Arch}
                build_cnode
                --manifest-in=-
                --elffile ${CDL_PP_ELF}
                --ccspace ${CDL_PP_CFILE}
        DEPENDS  ${capdl_python} ${manifest_in} )

    add_custom_command(OUTPUT ${CDL_PP_SO_CFILE}
        COMMAND ${python_with_capdl} ${manifest_in} |
        ${capdl_linker_tool}
                --arch=${KernelSel4Arch}
                build_so_cnode
                --manifest-in=-
                --sofile ${CDL_PP_SO}
                --socspace ${CDL_PP_SO_CFILE}
        DEPENDS  ${capdl_python} ${manifest_in})

    add_custom_target(${target_so} DEPENDS ${CDL_PP_SO_CFILE})
    add_custom_target(${target} DEPENDS ${CDL_PP_CFILE})
endfunction()


function(cdl_calc_relo progname soname symbolfile target)

    add_custom_command(OUTPUT ${symbolfile}
        COMMAND python3 ${CMAKE_SOURCE_DIR}/dl_build/dl/calc_relo.py ${progname} ${soname} ${symbolfile}
        COMMENT "Generating symbolfile for ${progname} with ${soname}"
        )

    add_custom_target(${target} DEPENDS ${symbolfile})
endfunction()
