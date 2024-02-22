#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

int main()
{
    ifstream file("data.txt");
    string target;
    cin >> target;
    map<string, int> wordsCount;
    string word;
    while (file >> word)
    {
        if (word == target)
        {
            string nextWord;
            file >> nextWord;

            if (nextWord != "stopword")
            {
                wordsCount[nextWord]++;
            }
        }
    }
    vector<pair<string, int>> sortedWords;
    for (const auto& pair : wordsCount)
    {
        sortedWords.emplace_back(pair.first, pair.second);
    }
    sort(sortedWords.begin(), sortedWords.end(), [](const auto& a, const auto& b) {
        return a.second != b.second ? a.second > b.second : a.first < b.first;
        });
    if (sortedWords.empty())
    {
        cout << "-" << endl;
    }
    else
    {
        for (int i = 0; i < 3 && i < sortedWords.size(); ++i)
        {
            cout << sortedWords[i].first << " ";
        }
        cout << endl;
    }
}
