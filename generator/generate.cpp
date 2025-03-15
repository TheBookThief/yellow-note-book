#include <bits/stdc++.h>
using namespace std;

int main()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(-20, 20), cnt(1, 5);

    int numPoly = 1815;
    for (int i = 1; i <= numPoly; i++)
    {
        ofstream out("polynoms" + to_string(i) + ".txt");

        int size = cnt(gen);
        for (int j = 1; j <= size; j++)
        {
            int sol = dist(gen);
            out << "(x";
            if (sol >= 0)
                out << "+";
            out << to_string(sol) << ")";
        }
        out << endl;
        out.close();
    }

    return 0;
}