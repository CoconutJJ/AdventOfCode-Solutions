#include <stdio.h>
#include <stdlib.h>

int main (int argc, char **argv)
{
        if (argc < 2) {
                fprintf (stderr, "error: expected input file.\n");
                exit (1);
        }

        int max = 0, curr_total = 0;

        FILE *fp = fopen (argv[1], "r");
        if (!fp) {
                perror ("fopen");
                exit (1);
        }

        char buffer[12]; // ceil(log10(2^32)) + 1 = 11 

        while (fgets (buffer, 12, fp) != NULL) {
                if (buffer[0] == '\n') {
                        max = curr_total > max ? curr_total : max;
                        curr_total = 0;
                        continue;
                }

                long value = strtol (buffer, NULL, 10);

                curr_total += (int)value;
        }

        printf ("%d\n", max);
}