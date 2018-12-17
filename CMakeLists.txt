#  ---------------------------------------------------------------------------------------------------------------------
#  The MIT License (MIT)
#
#  Copyright (c) 2018 Ralph-Gordon Paul. All rights reserved.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
#  Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#  ---------------------------------------------------------------------------------------------------------------------

cmake_minimum_required (VERSION 3.6)

set(CMAKE_C_STANDARD 11)

set(SQLITE3_VERSION "3240000" CACHE STRING "sqlite3 version")
set(SQLITE3_SRC "${CMAKE_CURRENT_LIST_DIR}/sqlite-amalgamation-${SQLITE3_VERSION}" CACHE STRING "sqlite3 source folder")

add_library(sqlite3
            STATIC
            "${SQLITE3_SRC}/sqlite3.c"
            )

install(TARGETS sqlite3
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(FILES
        "${SQLITE3_SRC}/sqlite3.h"
        "${SQLITE3_SRC}/sqlite3ext.h"
        DESTINATION include)
