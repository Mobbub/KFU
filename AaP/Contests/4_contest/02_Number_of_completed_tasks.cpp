#include <iostream>
#include <fstream>
#include "json.hpp"

using json = nlohmann::json;

int countCompletedTasks(json data, int userId) {
    int count = 0;
    for (const auto& project : data) {
        for (const auto& task : project["tasks"]) {
            if (task["user_id"] == userId && task["completed"] == true) {
                count++;
            }
        }
    }
    return count;
}

int main() {
    int userId;
    std::cin >> userId;
    std::ifstream inputFile("data.json");
    json data;
    inputFile >> data;
    int completedTasksCount = countCompletedTasks(data, userId);
    std::cout << completedTasksCount << std::endl;
}
