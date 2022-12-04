#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int priority (char c)
{
        if ('a' <= c && c <= 'z')
                return c - 'a' + 1;
        else if ('A' <= c && c <= 'Z')
                return c - 'A' + 27;
        else
                return 0;
}

uint64_t bitset (char *rucksack)
{
        uint64_t set = 0;

        for (char *c = rucksack; *c != '\0'; c++) {
                uint64_t pri = priority (*c);

                if (pri != 0)
                        set |= 1ULL << pri;
        }

        return set;
}

uint64_t bitscan_sum (uint64_t set)
{
        uint64_t total = 0;

        for (uint64_t i = 0; i < 64; i++) {
                if (set & (1ULL << i)) {
                        total += i;
                }
        }

        return total;
}

void part1 ()
{
        char line_buffer[255];
        uint64_t total = 0;
        while (fgets (line_buffer, 255, stdin) != NULL) {
                size_t len = strlen (line_buffer);

                char *newline = strrchr (line_buffer, '\n');

                if (newline)
                        *newline = '\0';

                char left[125];
                char right[125];

                char *end = line_buffer + len / 2;
                char buf = *end;
                *end = '\0';
                strcpy (left, line_buffer);
                *end = buf;
                strcpy (right, end);

                uint64_t left_set = bitset (left);
                uint64_t right_set = bitset (right);

                total += bitscan_sum (left_set & right_set);
        }

        printf ("Total: %d", total);
}

void part2 ()
{
        char line_buffer[255];

        int group_count = 0;

        uint64_t set = UINT64_MAX;
        uint64_t total = 0;

        while (fgets (line_buffer, 255, stdin) != NULL) {
                size_t len = strlen (line_buffer);

                char *newline = strrchr (line_buffer, '\n');

                if (newline)
                        *newline = '\0';

                set &= bitset (line_buffer);

                group_count++;

                if (group_count == 3) {
                        total += bitscan_sum(set);
                        set = UINT64_MAX;
                        group_count = 0;
                }
        }

        printf ("Total: %d", total);
}

int main (int argc, char **argv)
{
        part2();
        return 0;
}
