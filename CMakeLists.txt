# fichier contenant la fonction gerant les en-tetes precompilees
include(${CMAKE_CURRENT_SOURCE_DIR}/precompiled_headers.cmake)

cmake_minimum_required( VERSION 2.8.1 )
project(MICMAC)

if(POLICY CMP0020)
	cmake_policy(SET CMP0020 NEW) #windows specific: Automatically link Qt executables to qtmain
endif()

set(VERBOSE 0)

set (MICMAC_VERSION_MAJOR 1)
set (MICMAC_VERSION_MINOR 0)

##############################
## 			OPTIONS			##
##############################

# construire l'interface graphique
OPTION(WITH_INTERFACE  "build graphic interface" OFF)

# Utiliser Kakadu
OPTION(WITH_KAKADU  "Include KAKADU Support" OFF)

# Utiliser Ign orientation
OPTION(WITH_IGN_ORI "Include Ign orientation" OFF )

# Utiliser Ign orientation
OPTION(WITH_IGN_IMAGE "Include Ign image" OFF )

# Utiliser les en-tetes precompilees
OPTION(WITH_HEADER_PRECOMP "En-tetes precompilees" ON )

# Utiliser les en-tetes precompilees
OPTION(BUILD_ONLY_ELISE_MM3D "Projet Elise et MM3D uniquement" OFF )

# construire l'interface graphique
OPTION(WITH_ETALONPOLY  "Build etalonnage polygone" ON)

# construire les binaires Poisson
OPTION(BUILD_POISSON "Build Poisson binaries" OFF )

# construire le binaire Rnx2rtkp
OPTION(BUILD_RNX2RTKP "Build Rnx2rtkp binaries" OFF )

# Utiliser Cuda
OPTION(CUDA_ENABLED "Utilisation de cuda" OFF )

OPTION(WITH_OPENCL  "Utilisation d'OpenCL" OFF )

# Multi thread Poisson avec OpenMP
OPTION(WITH_OPEN_MP "use OpenMP" OFF )

# print system calls
OPTION(TRACE_SYSTEM "print system calls" OFF )

# compile low-level test bench
OPTION(BUILD_BENCH "compile low-level test bench" OFF )

# Interfaces de saisie des param�tres
OPTION(WITH_QT5 "compile Qt interfaces" OFF )

# Interfaces de saisie des param�tres
OPTION(WITH_QT4 "compile Qt 4 interfaces" OFF )

# Compilateur C++11
OPTION(WITH_CPP11 "Compilateur C++11" OFF )

OPTION(DEPLOY "compile for end-user" OFF)

OPTION(UPDATE_TRANSLATIONS "Update source translation translations/*.ts files (WARNING: make clean will delete the source .ts files! Danger!)")

if ( TRACE_SYSTEM )
	add_definitions(-D__TRACE_SYSTEM__=${TRACE_SYSTEM})
endif()

if (__DEBUG)
	add_definitions(-D__DEBUG=${__DEBUG})
endif()

if ( WITH_OPEN_MP )
	FIND_PACKAGE(OpenMP REQUIRED)
	if (${CUDA_ENABLED})
	    message("using OpenMP for Poisson 3d shell computing and Cuda precompute")
	else()
	    message("using OpenMP for Poisson 3d shell computing")
	endif()
	list( APPEND CMAKE_C_FLAGS ${OpenMP_C_FLAGS} )
	list( APPEND CMAKE_CXX_FLAGS ${OpenMP_CXX_FLAGS} )
	add_definitions(-DUSE_OPEN_MP)
endif()

# Utiliser Doxygen
OPTION(WITH_DOXYGEN "Generation de documentation" OFF )


######################################
## 	Trouver les EXES et Libs	##
######################################
if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
	add_definitions(-DELISE_Darwin)
	set(BIN_AUX_SUBDIR "darwin")
elseif (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
	set(BIN_AUX_SUBDIR "windows")
else()
	set(BIN_AUX_SUBDIR "linux")
endif()
set (BIN_AUX_FULL_PATH ${PROJECT_SOURCE_DIR}/binaire-aux/${BIN_AUX_SUBDIR})

# DEFINITIION : des chemins binaires sous UNIX
set(UnixBinPath
		/bin
		/usr/bin
		/usr/local/bin)

set(qt_version 0)
set(DEPLOY 0)
set(PROJECT_SRC_DIR \"${PROJECT_SOURCE_DIR}\" )

if(${WITH_QT5} OR ${WITH_QT4})
	find_package(OpenGL REQUIRED)

	if ( OPENGL_FOUND )
		message( STATUS "-----> OpenGL found" )

		if ( MSVC )
				include("${PROJECT_SOURCE_DIR}/src/saisieQT/FindWindowsSDK.txt")
				# ajoute /lib a tous les repertoires contenant un SDK
				foreach( sdk_dir ${WINDOWSSDK_DIRS} )
						list( APPEND SDK_LIB_DIRS "${sdk_dir}/lib" )
				endforeach()
				set( CMAKE_PREFIX_PATH "${SDK_LIB_DIRS}" )
				message (" WindowsSDKDir : " ${CMAKE_PREFIX_PATH} )
		endif()

		if (${WITH_QT5})
			    #find_package(Qt5 COMPONENTS Gui Core Widgets OpenGL LinguistTools Concurrent Xml)
			    #~ find_package(Qt5 COMPONENTS Gui Core OpenGL Xml)
			    find_package(Qt5Widgets REQUIRED)
			    find_package(Qt5Xml REQUIRED)
			    find_package(Qt5Concurrent REQUIRED)
			    #~ find_package(Qt5LinguistTools REQUIRED)
			    find_package(Qt5OpenGL REQUIRED)

			if (Qt5Widgets_FOUND)
				if (NOT QT_QMAKE_EXECUTABLE)
					get_target_property(QT_QMAKE_EXECUTABLE Qt5::qmake IMPORTED_LOCATION)
				endif()

				EXECUTE_PROCESS(
						COMMAND
						${QT_QMAKE_EXECUTABLE} -query QT_VERSION
						RESULT_VARIABLE qmake_version_result
						OUTPUT_VARIABLE QT_VERSION
						ERROR_QUIET
						OUTPUT_STRIP_TRAILING_WHITESPACE
					)

				message(STATUS "using Qt " ${QT_VERSION})

				if (QT_VERSION VERSION_LESS "5.4.0")
					message(STATUS "Qt version < 5.4.0: using shortcuts patch")
					add_definitions("-D__QT_5_SHORTCUT_PATCH")
				endif()

			    set(qt_version 5)

#                            set(QT_LIBRARIES
#                                    ${Qt5Core_LIBRARIES}
#                                    ${Qt5Gui_LIBRARIES}
#                                    ${Qt5Xml_LIBRARIES}
#                                    ${Qt5OpenGL_LIBRARIES}
#                            )

#                            message("${Qt5Core_LIBRARIES}")

			    #SET(QT_LIBRARY_DIRS "${Qt5_LIBRARY_DIRS}")

#                            link_directories(${Qt5_LIBRARY_DIRS})

			elseif(${WITH_QT5} AND NOT Qt5Widgets_FOUND)

			    message("WARNING QT 5 not found")
			    message("Set Qt5_DIR to qt CMAKE directory")
			    message("   Qt5_DIR --> C:\\Qt\\Qt5.0.1\\5.0.1\\msvc2010\\lib\\cmake\\Qt5")
			    message("   Qt5_DIR --> /opt/Qt5.x.x/5.x.x/gcc_64/lib/cmake/Qt5")

			endif()

		elseif (${WITH_QT4})

			FIND_PACKAGE(Qt4 QUIET COMPONENTS QtCore QtGui QtOpenGL QtXml)
			if( QT4_FOUND )
			    message( STATUS "-----> Qt4 found" )
			    set(qt_version 4)
			else()
			    message( "Qt not available, Qt graphical tools disabled" )
			    message( "**************************************************************************************************************************************" )
			    message( "If Qt is installed, please set QT_QMAKE_EXECUTABLE" )
			    message( "**************************************************************************************************************************************" )
			endif()

		endif()
	else()
		message( "OpenGL not available, Qt graphical tools disabled" )
	endif()
endif()

IF (${CMAKE_SYSTEM_NAME} MATCHES "Darwin" AND qt_version EQUAL 5)
	if (POLICY CMP0045)
		cmake_policy(SET CMP0045 NEW) # target of get_target_property must exists or a FATAL_ERROR is issued
	endif()

	if (NOT QT_INSTALL_LIBS)
		EXECUTE_PROCESS(
				COMMAND
				${QT_QMAKE_EXECUTABLE} -query QT_INSTALL_LIBS
				RESULT_VARIABLE qmake_install_libs_result
				OUTPUT_VARIABLE QT_INSTALL_LIBS
				ERROR_QUIET
				OUTPUT_STRIP_TRAILING_WHITESPACE
			)
	endif()

	if (NOT QT_INSTALL_PLUGINS)
		EXECUTE_PROCESS(
				COMMAND
				${QT_QMAKE_EXECUTABLE} -query QT_INSTALL_PLUGINS
				RESULT_VARIABLE qmake_install_plugins_result
				OUTPUT_VARIABLE QT_INSTALL_PLUGINS
				ERROR_QUIET
				OUTPUT_STRIP_TRAILING_WHITESPACE
			)
	endif()

	set(CMAKE_INSTALL_RPATH "${QT_INSTALL_LIBS}" "${QT_INSTALL_PLUGINS}" "@executable_path/../Frameworks")
endif()

if ( NOT ${qt_version} EQUAL 0 )
      message( STATUS "QT tools enabled (Qt" ${qt_version} ")" )
endif()

if (${DEPLOY})
    set(DEPLOY 1)
endif()

if(${WITH_CPP11})
    IF(NOT MSVC)
	    message("c++11")
	    # support c++11
	    ADD_DEFINITIONS(
		    -std=c++11 # Or -std=c++0x
		    # Other flags
	    )
    endif()
endif()

# CUDA
if (${CUDA_ENABLED})

	OPTION(CUDA_LINEINFO "Compilation avec lineInfo" OFF )
	OPTION(CUDA_FASTMATH "Compilation avec FASTMATH" OFF )
	OPTION(CUDA_CPP11THREAD_NOBOOSTTHREAD "Use c++11 for the multi-threading" OFF )
	OPTION(CUDA_NVTOOLS "Use NV TOOLS" OFF )


	FIND_PACKAGE(CUDA)
	INCLUDE(FindCUDA)

	if(CUDA_FOUND)


			SET(Cuda_Sample_path_Windows_VISTA_7_8 "$ENV{AllUsersProfile}/NVIDIA Corporation/CUDA Samples/v${CUDA_VERSION}/")
			SET(Cuda_Sample_path_Windows_XP "$ENV{AllUsersProfile}/Application Data/NVIDIA Corporation/CUDA Samples/v${CUDA_VERSION}/")
			SET(Cuda_Sample_path_Apple "/Developer/NVIDIA/CUDA-${CUDA_VERSION}/samples/")
			SET(Cuda_Sample_path_Linux "${CUDA_TOOLKIT_ROOT_DIR}/samples")

	    FIND_PATH(
			CUDA_SAMPLE_DIR
			NAMES
			    common/inc/helper_cuda.h
			PATHS
			    ${Cuda_Sample_path_Linux}
			    ${Cuda_Sample_path_Windows_VISTA_7_8}
							${Cuda_Sample_path_Windows_XP}
			    ${Cuda_Sample_path_Windows_Apple}
		     )

					#message(${CUDA_SAMPLE_DIR})

	    if(NOT CUDA_SAMPLE_DIR STREQUAL "CUDA_SAMPLE_DIR-NOTFOUND")
				#message("Cuda Samples Found")
		message("Cuda Samples Found : " ${CUDA_SAMPLE_DIR})
		INCLUDE_DIRECTORIES(${CUDA_SAMPLE_DIR}/common/inc)
	    else()
		message("Cuda Samples Dir Not Found, install cuda samples or set CUDA_SAMPLE_DIR")
	    endif()

	endif()


	#IFNOT(${WITH_IGN_ORI})

	# ne pas oublier boost_no_system_paths

	if (NOT ${CUDA_CPP11THREAD_NOBOOSTTHREAD})
		set(Boost_USE_STATIC_LIBS ON)
		set(Boost_NO_SYSTEM_PATHS ON)
		FIND_PACKAGE( Boost 1.48.0 COMPONENTS system serialization thread date_time chrono REQUIRED )
		#chrono
		 IF(NOT ${WITH_IGN_ORI})
			  include_directories ( ${Boost_INCLUDE_DIRS} )
			  include_directories ( ${Boost_INCLUDE_DIR} )
		 endif()
	else()
			if(MSVC AND NOT MSVC12 )
				message(FATAL_ERROR "This version of visual doesn't support c++11")
			endif()
	    if(NOT ${WITH_CPP11})
		SET(WITH_CPP11 ON CACHE BOOL "Compilateur C++11" FORCE)
		IF(NOT MSVC)
			message("c++11")
			# support c++11
			ADD_DEFINITIONS(
				-std=c++11 # Or -std=c++0x
				# Other flags
			)
		endif()
	    endif()
	endif()
endif()

# Etalonnage polygone

if (${WITH_ETALONPOLY})
	add_definitions(-DETA_POLYGON)
endif()

# MERCURIAL
find_program(MERCURIAL_EXECUTABLE hg DOC "Emplacement de gestionnaire de versions Mercurial")

if (NOT HG_REVISION_DIST)
	if(NOT MERCURIAL_EXECUTABLE)
		message( STATUS "Mercurial (hg) cannot be found" )
		set( HG_REVISION_DIST "unknown_no_hg" )
	else()
		# Affiche la revision MICMAC
		EXECUTE_PROCESS(
			COMMAND
			${MERCURIAL_EXECUTABLE} identify --num
			WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
			RESULT_VARIABLE hg_result
			OUTPUT_VARIABLE HG_REVISION_DIST
			ERROR_QUIET
			OUTPUT_STRIP_TRAILING_WHITESPACE
		)

		if ( ${hg_result} )
			set(HG_REVISION_DIST "unknown_hg_failed")
		endif()
	endif()
endif()
message( STATUS "Derniere revision mercurial de MicMac : " ${HG_REVISION_DIST})

set(HG_REV ${HG_REVISION_DIST} CACHE STRING "Revision" FORCE)

set( HG_REVISION_DIST \"${HG_REVISION_DIST}\" )
CONFIGURE_FILE (
	"include/general/HG_defines.h.in"
	"${CMAKE_SOURCE_DIR}/include/general/HG_defines.h"
)

CONFIGURE_FILE (
	"include/general/CMake_defines.h.in"
	"${CMAKE_SOURCE_DIR}/include/general/CMake_defines.h"
)

INCLUDE_DIRECTORIES(${PROJECT_BINARY_DIR}/include)

# Utiliser le driver Kakadu pour gerer les images JP2OOO
IF(${WITH_KAKADU})
	if(KAKADU_NO_FIND)
		# to use when FindKAKAKDU.cmake does not exist (KAKADU_DIR must be set)
		set( KAKADU_LIBRARY_DIRS "${KAKADU_DIR}/lib" )
		set( KAKADU_INCLUDE_DIRS "${KAKADU_DIR}/include" )
		set( KAKADU_LIBRARIES "kdu_v64R;kdu;kdu_aux" )
		# quick check of Kakadu's headers and libraries
		if ( ( (EXISTS "${KAKADU_LIBRARY_DIRS}/kdu.lib") OR
		       (EXISTS "${KAKADU_LIBRARY_DIRS}/libkdu.a") ) AND
		     ( EXISTS "${KAKADU_DIR}/include/jp2.h" ) )
			set( KAKADU_FOUND 1 )
		endif()
	else()
		FIND_PACKAGE( KAKADU )
	endif()

	IF(NOT KAKADU_FOUND)
		MESSAGE("Warning! Kakadu not found. Micmac will be built without JPEG2000 support.")
	ELSE()
		message( STATUS "Kakadu enabled" )
		ADD_DEFINITIONS(-D__USE_JP2__)
		LINK_DIRECTORIES( ${KAKADU_LIBRARY_DIRS})
		INCLUDE_DIRECTORIES( ${KAKADU_INCLUDE_DIRS} )
	ENDIF()
ENDIF()

# Utiliser le socle IGN pour gerer les orientations coniques ET/OU les images JP2000
IF(${WITH_IGN_ORI} OR ${WITH_IGN_IMAGE})
	SET(SOCLE_COMPONENTS "")
	IF(${WITH_IGN_ORI})
		SET(SOCLE_COMPONENTS orientation geodesy transform math numeric tools  data xml core)
	ENDIF()
	IF(${WITH_IGN_IMAGE})
		LIST(APPEND SOCLE_COMPONENTS image transform math numeric tools data xml core)

		#pour le DMR sinon on peut l'enlever aisni que la dependeance a Geos
		LIST(APPEND SOCLE_COMPONENTS geometry)
	ENDIF()

	FIND_PACKAGE( IgnSocle  COMPONENTS "${SOCLE_COMPONENTS}")
	FIND_PACKAGE(TinyXML)
	FIND_PACKAGE(PROJ4)

	if (${WITH_IGN_IMAGE})
		FIND_PACKAGE(GDAL)
		FIND_PACKAGE( KAKADU )
		FIND_PACKAGE(ECWJ2)
		FIND_PACKAGE(Geos)
	endif()

	FIND_PACKAGE( Boost 1.48.0 COMPONENTS unit_test_framework date_time filesystem system serialization thread regex chrono REQUIRED)

	#add_definitions( "-DBOOST_THREAD_USE_LIB" )
	add_definitions( "-DBOOST_TYPEOF_COMPLIANT" )
	add_definitions( "-DBoost_USE_STATIC_LIBS" )
	SET(Boost_USE_MULTITHREADED ON)
	SET(Boost_USE_STATIC_LIBS ON)

	SET(DEPENDENCIES "")
	IF(IgnSocle_FOUND AND TinyXML_FOUND AND Boost_FOUND AND ${WITH_IGN_ORI})
		ADD_DEFINITIONS(-D__USE_ORIENTATIONIGN__ )

		LIST(APPEND DEPENDENCIES  IgnSocle TinyXML Boost)
		IF ( PROJ4_FOUND )
			LIST(APPEND DEPENDENCIES PROJ4)
		ENDIF()
	ELSE()
		IF (${WITH_IGN_ORI})
			MESSAGE("IgnSocle_FOUND : ${IgnSocle_FOUND}")
	    MESSAGE("TinyXML_FOUND : ${TinyXML_FOUND}")
	    MESSAGE("Boost_FOUND : ${Boost_FOUND}")
			MESSAGE("Warning! Ign Orientation not found. Micmac will be built without Ign Orientation support.")
		ENDIF()
	ENDIF()

	IF(IgnSocle_FOUND AND TinyXML_FOUND AND Boost_FOUND AND GDAL_FOUND AND ${WITH_IGN_IMAGE})
		ADD_DEFINITIONS(-D__USE_IMAGEIGN__ )

		LIST(APPEND DEPENDENCIES IgnSocle TinyXML GDAL Boost)
		IF (KAKADU_FOUND)
			LIST(APPEND DEPENDENCIES KAKADU)
		ENDIF()
		IF (ECWJ2_FOUND)
			LIST(APPEND DEPENDENCIES ECWJ2)
		ENDIF()
		IF (Geos_FOUND)
			LIST(APPEND DEPENDENCIES Geos)
		ENDIF()
	ELSE()
		IF (${WITH_IGN_IMAGE})
			MESSAGE("IgnSocle_FOUND : ${IgnSocle_FOUND}")
			MESSAGE("TinyXML_FOUND : ${TinyXML_FOUND}")
			MESSAGE("GDAL_FOUND : ${GDAL_FOUND}")
			MESSAGE("KAKADU_FOUND : ${KAKADU_FOUND}")
			MESSAGE("ECWJ2_FOUND : ${ECWJ2_FOUND}")
			MESSAGE("Geos_FOUND : ${Geos_FOUND}")
			MESSAGE("Boost_FOUND : ${Boost_FOUND}")
			MESSAGE("Warning! Ign Image not found. Micmac will be built without Ign Image support.")
		ENDIF()
	ENDIF()

	foreach( DEPENDENCY ${DEPENDENCIES} )
		LINK_DIRECTORIES   (${${DEPENDENCY}_LIBRARY_DIRS})
		INCLUDE_DIRECTORIES(${${DEPENDENCY}_INCLUDE_DIRS})
		#message("LINK_DIR ${DEPENDENCY} --> ${${DEPENDENCY}_LIBRARY_DIRS}")
		#message("INCLUDE_DIR ${DEPENDENCY} --> ${${DEPENDENCY}_INCLUDE_DIRS}")
	endforeach()

ENDIF()

# Utiliser la librairie du MATIS pour gerer les orientations coniques
IF(${WITH_MATIS_ORI})
	FIND_PACKAGE( MatisOrientation )
	IF(NOT MatisOrientation_FOUND)
		MESSAGE("Warning! MatisOrientation not found. Micmac will be built without MatisOrientation support.")
	ELSE()
		OPTION(MICMAC_USE_PROJ4 "Use PROJ4" OFF)
		#-- recherche de boost
		SET(Boost_USE_MULTITHREADED ON)
		FIND_PACKAGE( Boost 1.48.0 COMPONENTS unit_test_framework date_time system filesystem serialization thread regex chrono REQUIRED)
		FIND_PACKAGE(TICPP REQUIRED)
		IF ( TICPP_FOUND)
			LINK_DIRECTORIES(${TICPP_LIBRARY_DIRS})
			INCLUDE_DIRECTORIES(${TICPP_INCLUDE_DIRS})
		ENDIF()

		IF (MICMAC_USE_PROJ4)
			FIND_PACKAGE( PROJ4 REQUIRED )
			LINK_DIRECTORIES(${PROJ4_LIBRARY_DIRS})
			INCLUDE_DIRECTORIES(${PROJ4_INCLUDE_DIRS})
		ENDIF()

		ADD_DEFINITIONS(-D__USE_ORIENTATIONMATIS__ )
		LINK_DIRECTORIES(${MatisOrientation_LIBRARY_DIRS})
		INCLUDE_DIRECTORIES(${MatisOrientation_INCLUDE_DIRS})

	ENDIF()
ENDIF()


# VERIFICATION si ImageMagick est installe

if(NOT WIN32) # ImageMagick n'est pas obligatoire sous windows puisque les ex�cutables n�cessaire sont fournis
	find_package(ImageMagick QUIET)

	if(NOT ImageMagick_FOUND)
			MESSAGE("\n***   ATTENTION!!! Vous devez installer Image Magick. ***")
			MESSAGE("***   http://www.imagemagick.org/script/index.php     ***\n")
	endif(NOT ImageMagick_FOUND)
endif()

if (MINGW)
	add_definitions(-D__MINGW__ -D__MSVCRT_VERSION__=0x800 -D_WIN32_WINNT=0x0500)
	set( WINSOCK2_LIBRARY ws2_32 )
endif()

if(NOT WIN32)

	# VERIFICATION si Proj4 est installe
	#find_program(PROJ4_EXECUTABLE proj4 PATHS ${UnixBinPath} )
	if(PROJ4_EXECUTABLE_FOUND)

		message("Proj4 non trouve!!")

	endif()

	# VERIFICATION si X11 est present sous MacOS et Linux
	OPTION(NO_X11  "ignoring X11 libraries even if existing" OFF)

	IF (NOT NO_X11)
		#message("Trying to find X11 package�")
		FIND_PACKAGE(X11)
	ELSE()
		message("Ignoring X11 package...")
		set(X11_LIBRARY_DIR "") # au cas ou on ait fait une passe de cmake sans actier 'NO_X11'
	ENDIF()

	IF ( ${CMAKE_SYSTEM_NAME} MATCHES "Linux" )
		set( DYN_LIB_LIBRARY dl )
	endif()

	IF (X11_FOUND)
		#message("X11 Found : ")
		#message("   include dir   : " ${X11_INCLUDE_DIR} )
		#message("   libraries     : " ${X11_LIBRARIES} )
		#message("   libraries dir : " ${X11_LIBRARY_DIR} )
	INCLUDE_DIRECTORIES( ${X11_INCLUDE_DIR} )
	ELSE()
		add_definitions(-DNO_X11)
		MESSAGE("X11 Not Found : pas de SaisieMasq")
	ENDIF()
ELSE()
	set( CMAKE_BUILD_TYPE Release )
ENDIF()

# DEFINITION : des preprocesseurs windows
IF (MSVC)
	set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /LARGEADDRESSAWARE" )
	# Zm131 -> Erreur de compilation sous windows 7 avec Cuda et Boost
	if (${CUDA_ENABLED})
	    add_definitions( "/W3 /D_CRT_SECURE_NO_WARNINGS /wd4005 /wd4996 /wd4661 /wd4267 /wd4355 /nologo" )
	#else()
	    add_definitions( "/W3 /D_CRT_SECURE_NO_WARNINGS /wd4005 /wd4996 /wd4661 /wd4267 /nologo" )
	    # la valeur par defaut Zm1000 genere une erreur sous windows XP
			set(zm_value "/Zm200")
			string( FIND "${CMAKE_CXX_FLAGS}" "/Zm1000" has_zm1000 )
			if ( ${has_zm1000} LESS 0 )
				# la valeur par defaut Zm1000 n'existe plus a partir de la version 2.8.11
				set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${zm_value}")
			else()
				# REPLACE pour eviter le conflit Zm1000 vs ZmXXX
				string(REPLACE "/Zm1000" ${zm_value} CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})
			endif()
	elseif (NOT (CMAKE_CXX_COMPILER_VERSION VERSION_LESS "19.0.0")) # 19 is visual studio 2015
		set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zm263")
	elseif ( ${CMAKE_SYSTEM_VERSION} MATCHES "5.1" )
		set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zm131") # 5.1 is windows xp
	else()
		set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zm170")
	endif()

	if(NOT (CMAKE_CXX_COMPILER_VERSION VERSION_LESS "8.0.0"))
		SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP")
	endif()
ENDIF()

# DEFINITION : Dossier include
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/include)

# DEFINITION : des preprocesseurs G++
IF (CMAKE_COMPILER_IS_GNUCC)
	ADD_DEFINITIONS(-O2 -Wall)
ENDIF()

# DEFINITION : Windows : le projet debug est genere directement sous bin pour avoir les informations de Debug

IF (MSVC)
	 set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/bin)
	 set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR}/bin)
endif()


set(BUILD_PATH_BIN  ${PROJECT_SOURCE_DIR}/bin CACHE PATH "binaires install path")
set(BUILD_PATH_LIB  ${PROJECT_SOURCE_DIR}/lib CACHE PATH "library install path")

# DEFINITION : du dossier d'installation
set(Install_Dir		${BUILD_PATH_BIN})
set(Install_Dir_lib ${BUILD_PATH_LIB})

# DEFINITION : du dossier des sources d'Elise
set(ELISE_DIR src)

# CONSTRUCTION : Librairie ANN
include(${PROJECT_SOURCE_DIR}/CodeExterne/ANN/CMakeLists.txt)
# CONSTRUCTION : Librairie POISSON
include(${PROJECT_SOURCE_DIR}/CodeExterne/Poisson/CMakeLists.txt)
# CONSTRUCTION : Librairie Rnx2rtkp
include(${PROJECT_SOURCE_DIR}/CodeExterne/rnx2rtkp/CMakeLists.txt)
# CONSTRUCTION : Librairie ELISE
set( code_genere_dir ${PROJECT_SOURCE_DIR}/CodeGenere )
include(${code_genere_dir}/Sources.cmake)
ADD_SUBDIRECTORY(${ELISE_DIR})

# Doxygen
if(${WITH_DOXYGEN})
    find_package(Doxygen)
    if(DOXYGEN_FOUND)
	  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY)
	  add_custom_target(doc ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR} COMMENT "Generating API documentation with Doxygen" VERBATIM)
    endif(DOXYGEN_FOUND)
endif()

if ( ${BUILD_BENCH} )
   include(${PROJECT_SOURCE_DIR}/BenchElise/bench/CMakeLists.txt)
   include(${PROJECT_SOURCE_DIR}/BenchElise/bench_mm3d/CMakeLists.txt)
endif()
