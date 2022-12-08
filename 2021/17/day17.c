#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#define MIN(x, y) ((x) < (y) ? (x) : (y))
#define MAX(x, y) ((x) > (y) ? (x) : (y))

struct coord {
        int x;
        int y;
};

struct coord velocity_next(int x, int y)
{
        if (x < 0) {
                x = x + 1;
        } else if (x > 0) {
                x = x - 1;
        }
        y = y - 1;

        return (struct coord){ .x = x, .y = y };
}

int within_area(int x1, int x2, int y1, int y2, struct coord c)
{
        return c.x >= MIN(x1, x2) && c.x <= MAX(x1, x2) && c.y >= MIN(y1, y2) && c.y <= MAX(y1, y2);
}

int run_sim(struct coord velocity, int x1, int x2, int y1, int y2)
{
        struct coord pos = { .x = 0, .y = 0 };

        int maxY = INT_MIN;

        while (1) {
                maxY = MAX(maxY, pos.y);
                pos.x += velocity.x;
                pos.y += velocity.y;

                if (within_area(x1, x2, y1, y2, pos))
                        return maxY;

                if (velocity.x == 0 && pos.y < MIN(y1, y2))
                        return INT_MIN;

                velocity = velocity_next(velocity.x, velocity.y);
        }
}

int main(int argc, char **argv)
{
        int maxY = INT_MIN;

        for (int x = -137; x < 137 + 1; x++) {
                for (int y = -176; y < 176 + 1; y++) {
                        int height = run_sim((struct coord){ .x = x, .y = y }, 79, 137, -176, -117);
                        maxY = MAX(maxY, height);
                }
        }

        printf("%d", maxY);
}