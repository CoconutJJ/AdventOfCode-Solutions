#include <iostream>
#include <queue>
#include <string>

typedef std::pair<int, int> IntegerPair;
typedef std::pair<IntegerPair, int> QueueElement;

class Compare {
    public:
        bool operator() (QueueElement a, QueueElement b)
        {
                return a.second < b.second;
        }
};

int main (int argc, char **argv)
{
        if (argc < 2) {
                std::cerr << "Missing file name parameter.";
                exit (EXIT_FAILURE);
        }

        std::priority_queue<QueueElement, std::vector<QueueElement>, Compare>
                queue;

        return 0;
}