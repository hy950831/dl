
# @TAG(DATA61_BSD)
cmake_minimum_required(VERSION 3.7.2)
# declare the dl CMake project and the languages it is written in (just C)
project(dl C)

include(${KERNEL_HELPERS_PATH})
GenerateSimulateScript()

set(PLATFORM "x86_64" CACHE STRING "Platform to test")
set(RELEASE OFF CACHE BOOL "Performance optimized build")
set(VERIFICATION OFF CACHE BOOL "Only verification friendly kernel features")
set(PRINTING ON CACHE BOOL "Printing feature")

set_property(CACHE PLATFORM PROPERTY STRINGS ${KernelX86Sel4Arch_all_strings} ${KernelARMPlatform_all_strings} ${KernelRiscVPlatform_all_strings})

# Determine the platform/architecture
if (${PLATFORM} IN_LIST KernelX86Sel4Arch_all_strings)
    set(KernelArch x86 CACHE STRING "" FORCE)
    set(KernelX86Sel4Arch ${PLATFORM} CACHE STRING "" FORCE)
elseif(${PLATFORM} IN_LIST KernelRiscVPlatform_all_strings)
    set(KernelArch riscv CACHE STRING "" FORCE)
    set(KernelRiscVPlatform ${PLATFORM} CACHE STRING "" FORCE)
    if(RISCV64)
        set(KernelRiscVSel4Arch "riscv64" CACHE STRING "" FORCE)
    else()
        set(KernelRiscVSel4Arch "riscv32" CACHE STRING "" FORCE)
    endif()
else()
    if (NOT ${PLATFORM} IN_LIST KernelARMPlatform_all_strings)
        message(FATAL_ERROR "Unknown PLATFORM. Initial configuration may not work")
    endif()
    set(KernelArch arm CACHE STRING "" FORCE)
    set(KernelARMPlatform ${PLATFORM} CACHE STRING "" FORCE)

    if(ARM_HYP)
        set(KernelArmHypervisorSupport ON CACHE BOOL "" FORCE)
    endif()

    if(AARCH64)
        set(KernelArmSel4Arch "aarch64" CACHE STRING "" FORCE)
    elseif(AARCH32)
        set(KernelArmSel4Arch "aarch32" CACHE STRING "" FORCE)
        if(ARM_HYP)
            set(KernelArmSel4Arch "arm_hyp" CACHE STRING "" FORCE)
        endif()
    endif()

    # Elfloader settings that correspond to how Data61 sets its boards up.
    ApplyData61ElfLoaderSettings(${KernelARMPlatform} ${KernelArmSel4Arch})
endif()

# libsel4 settings
# For the tutorials that do initialize the plat support serial printing they still
# just want to use the kernel debug putchar if it exists
set(LibSel4PlatSupportUseDebugPutChar TRUE CACHE BOOL "" FORCE)
# Just let the regular abort spin without calling DebugHalt to prevent needless
# confusing output from the kernel for a tutorial
set(LibSel4MuslcSysDebugHalt FALSE CACHE BOOL "" FORCE)

ApplyCommonReleaseVerificationSettings(${RELEASE} ${VERIFICATION})

if(SIMULATION)
    ApplyCommonSimulationSettings(${KernelArch})
else()
    if(KernelArchX86)
        set(KernelIOMMU ON CACHE BOOL "" FORCE)
    endif()
endif()

# Name the executable and list source files required to build it
add_executable(dl src/main.c)

# List of libraries to link with the application.
target_link_libraries(dl
    sel4
    muslc utils
    sel4muslcsys sel4utils
    sel4platsupport sel4debug
    )

# Tell the build system that this application is the root task.
DeclareRootserver(dl)
