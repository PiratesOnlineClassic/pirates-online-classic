gcc -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 -DMINOR_VERSION=0 -I/usr/include -I/usr/include/python2.7 -lstdc++ -lssl -lcrypto  -c ../nirai/src/aes.cxx -c -o ../nirai/src/aes.o

gcc -shared ../nirai/src/aes.o -L/usr/local/lib -lstdc++ -lssl -lcrypto -o ../nirai/src/aes.so
