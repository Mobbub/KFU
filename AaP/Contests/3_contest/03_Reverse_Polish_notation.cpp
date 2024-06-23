#include <iostream>
#include <stack>
#include <string>

using namespace std;

bool isOperator(char c)
{
    return c == '+' || c == '-' || c == '*' || c == '/' || c == '%' || c == '^';
}

int getPriority(char operation)
{
    if (operation == '+' || operation == '-')
    {
        return 1;
    }
    else if (operation == '*' || operation == '/' || operation == '%')
    {
        return 2;
    }
    else if (operation == '^')
    {
        return 3;
    }
    return 0;
}

string infixToPostfix(const string& infix)
{
    string postfix;
    stack<char> operators;

    for (char c : infix)
    {
        if (isdigit(c))
        {
            postfix += c;
        }
        else if (c == '(')
        {
            operators.push(c);
        }
        else if (c == ')')
        {
            while (!operators.empty() && operators.top() != '(')
            {
                postfix += " ";
                postfix += operators.top();
                operators.pop();
            }

            operators.pop(); // remove '('
        }
        else if (isOperator(c))
        {
            while (!operators.empty() && (getPriority(operators.top()) > getPriority(c)
                || (getPriority(operators.top()) == getPriority(c) && c != '^')))
            {
                postfix += " ";
                postfix += operators.top();
                operators.pop();
            }

            postfix += " ";
            operators.push(c);
        }
    }

    while (!operators.empty())
    {
        postfix += " ";
        postfix += operators.top();
        operators.pop();
    }

    return postfix;
}

int main()
{
    string infixExpression;
    getline(cin, infixExpression);

    string postfixExpression = infixToPostfix(infixExpression);

    cout << postfixExpression << endl;
}
