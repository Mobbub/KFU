#include <string>
#include <vector>

#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>
#include <mongocxx/uri.hpp>

struct User
{
    std::string surname;
    std::string group;
    std::string position;
};

std::vector<User> make_users_list()
{
    mongocxx::instance inst{};
    mongocxx::client connection{ mongocxx::uri{"mongodb+srv://Aboba:1van@ivan.vi217jg.mongodb.net/?retryWrites=true&w=majority"} };
    mongocxx::v_noabi::collection collection = connection["schedule"]["users"];

    std::vector<User> users;

    mongocxx::cursor cursor = collection.find({});

    for (const bsoncxx::v_noabi::document::view& document : cursor)
    {
        bsoncxx::document::element surname = document["surname"];
        bsoncxx::document::element group = document["groupe"];
        bsoncxx::document::element role = document["position"];

        User user;

        user.surname = std::string{ surname.get_string().value };
        user.group = std::string{ group.get_string().value };
        user.position = std::string{ role.get_string().value };

        users.push_back(user);
    }

    return users;
}

std::vector<User> make_admins_list(std::vector<User> users)
{
    std::vector<User> admins;

    for (const auto& user : users)
    {
        if (user.position == "Admin")
        {
            admins.push_back(user);
        }
    }

    return admins;
}

bool is_in_admins_list(const std::string& surname, const std::vector<User>& admins)
{
    for (const auto& admin : admins)
    {
        if (admin.surname == surname)
        {
            return true;
        }
    }

    return false;
}