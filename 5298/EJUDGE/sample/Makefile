### BEGIN ejudge auto-generated makefile ###
EJUDGE_PREFIX_DIR ?= /opt/ejudge
EJUDGE_CONTESTS_HOME_DIR ?= /home/judges
EJUDGE_LOCAL_DIR ?= /var/lib/ejudge
EJUDGE_SERVER_BIN_PATH ?= /opt/ejudge/libexec/ejudge/bin

CXX = g++
CXXFLAGS = -O2 -std=gnu++14
CXXLIBCHECKERFLAGS = -DEJUDGE -Wall -g -O2 -std=gnu++11

EXECUTE = ${EJUDGE_PREFIX_DIR}/bin/ejudge-execute
EXECUTE_FLAGS =  --use-stdin --use-stdout --test-pattern=%02d --corr-pattern=%02d.a --group=olympiads --time-limit=2

NORMALIZE = ${EJUDGE_SERVER_BIN_PATH}/ej-normalize
NORMALIZE_FLAGS = --workdir=tests --test-pattern=%02d --corr-pattern=%02d.a --group=olympiads

all : sol_ik_ac checker
check_settings : all normalize

sol_ik_ac : sol_ik_ac.cpp
	${CXX} -DEJUDGE ${CXXFLAGS} sol_ik_ac.cpp -osol_ik_ac ${CXXLIBS}

checker : checker.cpp
	${CXX} -DEJUDGE ${CXXLIBCHECKERFLAGS} checker.cpp -ochecker ${CXXLIBCHECKERLIBS}

answers : sol_ik_ac
	${EXECUTE} ${EXECUTE_FLAGS} --update-corr --test-dir=tests --workdir=tests --all-tests sol_ik_ac

answer : sol_ik_ac
	cd tests && ${EXECUTE} ${EXECUTE_FLAGS} --update-corr --test-num=${TEST_NUM} ../sol_ik_ac


normalize :
	${NORMALIZE} ${NORMALIZE_FLAGS} --all-tests

clean :
	-rm -f *.o *.class *.exe *~ *.bak sol_ik_ac checker

### END ejudge auto-generated makefile ###
