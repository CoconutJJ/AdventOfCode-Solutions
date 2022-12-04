
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define BYTE_BUFFER_SIZE 10

char buffer[BYTE_BUFFER_SIZE];

uint8_t hexCharToBin(char c) {

    if ('0' <= c <= '9') {
        return c - '0';
    }

    if ('a' <= c <= 'f') {
        return c - 'a' + 10;
    }

    if ('A' <= c <= 'F') {
        return c - 'F' + 10;
    }
}

int readBits(int n) {

    

}




int main(int argc, char **argv)
{

}
