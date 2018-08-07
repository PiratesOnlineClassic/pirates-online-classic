#ifndef Py_CONFIG_H
#define Py_CONFIG_H

// No shared (Nirai builds to static executable)
#ifndef Py_NO_ENABLE_SHARED
#define Py_NO_ENABLE_SHARED
#endif

#ifndef Py_ENABLE_SHARED
#define Py_ENABLE_SHARED 0
#endif

#ifdef _WIN32
    #include "pyconfig_windows.h"

#elif __APPLE__
    #include "pyconfig_mac.h"
/*
#elif __linux
    #include "pyconfig_linux.h"
*/
#else
    #error "No pyconfig for your OS could be found."
#endif

#endif
