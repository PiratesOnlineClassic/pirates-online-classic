cmake_minimum_required(VERSION 2.8.5 FATAL_ERROR)
project(pythonembed)

if(WIN32)
	add_definitions(-DWIN32)
	add_definitions(-D_WIN32)
	add_definitions(-D_USRDLL)
	add_definitions(-D_CRT_SECURE_NO_WARNINGS)
	add_definitions(-D_WINSOCK_DEPRECATED_NO_WARNINGS)
endif()

add_definitions(-DNDEBUG)
add_definitions(-DPy_NO_ENABLE_SHARED)
add_definitions(-DPy_BUILD_CORE)

set(OBJECTS_FILES
    Objects/abstract.c
    Objects/boolobject.c
    Objects/bufferobject.c
    Objects/bytearrayobject.c
    Objects/bytes_methods.c
    Objects/capsule.c
    Objects/cellobject.c
    Objects/classobject.c
    Objects/cobject.c
    Objects/codeobject.c
    Objects/complexobject.c
    Objects/descrobject.c
    Objects/dictobject.c
    Objects/enumobject.c
    Objects/exceptions.c
    Objects/fileobject.c
    Objects/floatobject.c
    Objects/frameobject.c
    Objects/funcobject.c
    Objects/genobject.c
    Objects/intobject.c
    Objects/iterobject.c
    Objects/listobject.c
    Objects/longobject.c
    Objects/memoryobject.c
    Objects/methodobject.c
    Objects/moduleobject.c
    Objects/object.c
    Objects/obmalloc.c
    Objects/rangeobject.c
    Objects/setobject.c
    Objects/sliceobject.c
    Objects/stringobject.c
    Objects/structseq.c
    Objects/tupleobject.c
    Objects/typeobject.c
    Objects/unicodectype.c
    Objects/unicodeobject.c
    Objects/weakrefobject.c
)

set(PARSER_FILES
    Parser/acceler.c
    Parser/bitset.c
    Parser/firstsets.c
    Parser/grammar.c
    Parser/grammar1.c
    Parser/listnode.c
    Parser/metagrammar.c
    Parser/myreadline.c
    Parser/node.c
    Parser/parser.c
    Parser/parsetok.c
    Parser/tokenizer.c
)

if(WIN32)
    set(PC_FILES
        PC/import_nt.c
        PC/msvcrtmodule.c
        PC/winsound.c
        PC/_subprocess.c
        PC/_winreg.c
    )
else()
    set(PC_FILES) # Empty
endif()

set(PYTHON_FILES
    Python/asdl.c
    Python/ast.c
    Python/atof.c
    Python/bltinmodule.c
    Python/ceval.c
    Python/codecs.c
    Python/compile.c
    Python/config.c
    Python/dtoa.c
    Python/dynload_stub.c
    Python/errors.c
    Python/formatter_string.c
    Python/formatter_unicode.c
    Python/frozen.c
    Python/frozenmain.c
    Python/future.c
    Python/getargs.c
    Python/getcompiler.c
    Python/getcopyright.c
    Python/getopt.c
    Python/getplatform.c
    Python/getversion.c
    Python/graminit.c
    Python/import.c
    Python/importdl.c
    Python/marshal.c
    Python/modsupport.c
    Python/mysnprintf.c
    Python/mystrtoul.c
    Python/peephole.c
    Python/pyarena.c
    Python/pyctype.c
    Python/pyfpe.c
    Python/pymath.c
    Python/pystate.c
    Python/pystrcmp.c
    Python/pystrtod.c
    Python/Python-ast.c
    Python/pythonrun.c
    Python/random.c
    Python/strdup.c
    Python/strtod.c
    Python/structmember.c
    Python/symtable.c
    Python/sysmodule.c
    Python/thread.c
    Python/traceback.c
    Python/_warnings.c
)

set(MODULES_FILES
    Modules/arraymodule.c
    Modules/audioop.c
    Modules/binascii.c
    Modules/cgensupport.c
    Modules/cmathmodule.c
    Modules/cPickle.c
    Modules/cryptmodule.c
    Modules/cStringIO.c
    Modules/datetimemodule.c
    Modules/errnomodule.c
    Modules/fpectlmodule.c
    Modules/fpetestmodule.c
    Modules/future_builtins.c
    Modules/gcmodule.c
    Modules/getbuildinfo.c
    Modules/getpath.c
    Modules/imageop.c
    Modules/itertoolsmodule.c
    Modules/mathmodule.c
    Modules/md5.c
    Modules/md5module.c
    Modules/mmapmodule.c
    Modules/operator.c
    Modules/parsermodule.c
    Modules/posixmodule.c
    Modules/puremodule.c
    Modules/python.c
    Modules/rotatingtree.c
    Modules/selectmodule.c
    Modules/sha256module.c
    Modules/sha512module.c
    Modules/shamodule.c
    Modules/signalmodule.c
    Modules/socketmodule.c
    Modules/stropmodule.c
    Modules/symtablemodule.c
    Modules/threadmodule.c
    Modules/timemodule.c
    Modules/unicodedata.c
    Modules/xxmodule.c
    Modules/xxsubtype.c
    Modules/yuvconvert.c
    Modules/zipimport.c
    Modules/zlibmodule.c
    Modules/_bisectmodule.c
    Modules/_codecsmodule.c
    Modules/_collectionsmodule.c
    Modules/_csv.c
    Modules/_functoolsmodule.c
    Modules/_hashopenssl.c
    Modules/_heapqmodule.c
    Modules/_json.c
    Modules/_localemodule.c
    Modules/_lsprof.c
    Modules/_math.c
    Modules/_randommodule.c
    Modules/_sre.c
    Modules/_ssl.c
    Modules/_struct.c
    Modules/_weakref.c
)

set(MODULES_IO_FILES
    Modules/_io/bufferedio.c
    Modules/_io/bytesio.c
    Modules/_io/fileio.c
    Modules/_io/iobase.c
    Modules/_io/stringio.c
    Modules/_io/textio.c
    Modules/_io/_iomodule.c
)

set(MODULES_CJKCODECS_FILES
    Modules/cjkcodecs/multibytecodec.c
    Modules/cjkcodecs/_codecs_cn.c
    Modules/cjkcodecs/_codecs_hk.c
    Modules/cjkcodecs/_codecs_iso2022.c
    Modules/cjkcodecs/_codecs_jp.c
    Modules/cjkcodecs/_codecs_kr.c
    Modules/cjkcodecs/_codecs_tw.c
)

include_directories(Include)
include_directories(Python)
if(WIN32)
    include_directories(PC)
endif()

include_directories(../panda3d/thirdparty/win-libs-vc10/openssl/include)
include_directories(../panda3d/thirdparty/win-libs-vc10/zlib/include)

source_group("Objects" FILES ${OBJECTS_FILES})
source_group("Parser" FILES ${PARSER_FILES})

if(WIN32)
    source_group("PC" FILES ${PC_FILES})
endif()

source_group("Python" FILES ${PYTHON_FILES})
source_group("Modules" FILES ${MODULES_FILES})
source_group("Modules IO" FILES ${MODULES_IO_FILES})
source_group("Modules cjkcodecs" FILES ${MODULES_CJKCODECS_FILES})

set(_FILES
    ${OBJECTS_FILES}
    ${PARSER_FILES}
    ${PYTHON_FILES}
    ${MODULES_FILES}
    ${MODULES_IO_FILES}
    ${MODULES_CJKCODECS_FILES}
)

if(WIN32)
    LIST(APPEND _FILES ${PC_FILES})
endif()

add_library(pythonembed STATIC ${_FILES})
