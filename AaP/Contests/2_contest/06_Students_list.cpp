#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

Student make_student(const string& line)
{
    string name, group;
    size_t pos = line.find(';');
    name = line.substr(0, pos);
    group = line.substr(pos + 1);
    Student student;
    student.name = name;
    student.group = group;
    return student;
}

bool is_upper(const Student& student1, const Student& student2)
{
    if (student1.group.compare(student2.group) < 0)
        return true;
    else if (student1.group.compare(student2.group) == 0)
    {
        if (student1.name.compare(student2.name) < 0)
            return true;
    }
    return false;
}

void print(const vector<Student>& students)
{
    if (students.empty())
    {
        cout << "Empty list!" << endl;
        return;
    }
    string current_group = students[0].group;
    cout << current_group << endl;
    for (const Student& student : students)
    {
        if (student.group != current_group)
        {
            current_group = student.group;
            cout << current_group << endl;
        }
        cout << "- " << student.name << endl;
    }
}
