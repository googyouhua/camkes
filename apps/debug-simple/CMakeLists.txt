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

cmake_minimum_required(VERSION 3.7.2)

project(debug-simple C)

DeclareCAmkESComponent(Client SOURCES client.c)
DeclareCAmkESComponent(Echo SOURCES echo.c)

# We need to preprocess our .camkes spec to insert the debug components
set(CAmkESCPP ON CACHE BOOL "" FORCE)

# Need support for the hardware debug API
set(HardwareDebugAPI ON CACHE BOOL "" FORCE)

# Only support ia32 at the moment
if(
    NOT
    "${KernelArch}"
    STREQUAL
    "x86"
    OR
        NOT
        "${KernelX86Sel4Arch}"
        STREQUAL
        "ia32"
)
    message(FATAL_ERROR "debug-simple application only supported on ia32")
endif()

# Since we cannot use generator expressions in CPP_FLAGS we have to hard code the include path
# that we want
DeclareCAmkESRootserver(
    debug-simple.camkes CPP_FLAGS -I${CMAKE_SOURCE_DIR}/projects/camkes-tool/libsel4camkes/include
)
