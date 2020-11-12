all: duplicate.c
	cc -c duplicate.c -fpic -I /usr/include/postgresql/12/server/
	cc -shared -o duplicate.so duplicate.o
