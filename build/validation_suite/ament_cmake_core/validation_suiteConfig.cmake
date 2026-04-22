# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_validation_suite_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED validation_suite_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(validation_suite_FOUND FALSE)
  elseif(NOT validation_suite_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(validation_suite_FOUND FALSE)
  endif()
  return()
endif()
set(_validation_suite_CONFIG_INCLUDED TRUE)

# output package information
if(NOT validation_suite_FIND_QUIETLY)
  message(STATUS "Found validation_suite: 0.0.1 (${validation_suite_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'validation_suite' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${validation_suite_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(validation_suite_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${validation_suite_DIR}/${_extra}")
endforeach()
