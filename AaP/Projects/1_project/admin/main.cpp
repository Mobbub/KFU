#include <iostream>
#include <direct.h>
#include <httplib.h>
#include <cookie.h>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/json.hpp>
#include "users_list.hpp"

using namespace httplib;

using bsoncxx::builder::stream::document;
using bsoncxx::builder::stream::open_document;
using bsoncxx::builder::stream::close_document;

std::string generateCookie(int cookie_size)
{
    std::string letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    std::string new_cookie = "";

    std::mt19937 generator(std::chrono::system_clock::now().time_since_epoch().count());

    for (int i = 0; i < cookie_size; i++)
    {
        std::uniform_int_distribution<int> distribution(0, letters.length() - 1);
        int randomIndex = distribution(generator);
        new_cookie += letters[randomIndex];
    }

    return new_cookie;
}

using session_data = std::map<std::string, std::string>;
std::map<std::string, session_data> sessions;

mongocxx::client connection{ mongocxx::uri{"mongodb+srv://Aboba:1van@ivan.vi217jg.mongodb.net/?retryWrites=true&w=majority"} };
mongocxx::v_noabi::collection collection = connection["schedule"]["users"];

std::vector<User> users = make_users_list();

httplib::Server::Handler loginÑheck(httplib::Server::Handler next);
void loginHandler(const Request& req, Response& res);
void homeHandler(const Request& req, Response& res);
void logoutHandler(const Request& req, Response& res);
void updateRoleHandler(const Request& req, Response& res);
void deleteUserHandler(const Request& req, Response& res);
void uploadFileHandler(const Request& req, Response& res);
void sendFileHandler(const Request& req, Response& res);

int main()
{
    Server server;
    server.Get("/", loginÑheck(homeHandler));
    server.Get("/login", loginÑheck(loginHandler));
    server.Post("/login", loginÑheck(loginHandler));
    server.Get("/logout", loginÑheck(logoutHandler));
    server.Post("/update-role", loginÑheck(updateRoleHandler));
    server.Post("/delete-user", loginÑheck(deleteUserHandler));
    server.Post("/upload-file", loginÑheck(uploadFileHandler));
    server.Post("/send-file", loginÑheck(sendFileHandler));

    server.listen("0.0.0.0", 8085);
}

static bool is_session_exist(const Request& req)
{
    auto cookie = Cookie::get_cookie(req, "user_cookie");

    if (cookie.name == "") return false;

    if (sessions.count(cookie.value) == 0) return false;

    return true;
}

httplib::Server::Handler loginÑheck(httplib::Server::Handler next)
{
    return [next](const Request& req, Response& res)
    {
        if (!is_session_exist(req) && req.path != "/login")
        {
            res.set_redirect("/login");
            return;
        }

        if (is_session_exist(req) && req.path == "/login")
        {
            res.set_redirect("/");
            return;
        }

        next(req, res);
    };
}

void loginHandler(const Request& req, Response& res)
{
    if (req.method == "GET")
    {
        std::string page = u8R"#(
            <!DOCTYPE html>
            <html>
            <head>
		        <meta charset="UTF-8">
		        <meta name="viewport" content="width=device-width, initial-scale=1.0">
		        <title>Login page</title>
                <style>
                    body {
                        background-color: #f0f0f0;
                        font-family: Arial, sans-serif;
                    }
                    .mainContainer {
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        padding: 20px;
                        background-color: #fff;
                        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
                        border-radius: 10px;
                    }
                    label {
                        display: inline-block;
                        margin-bottom: 5px;
                    }
                    input[type="text"], input[type="password"] {
                        width: 94%;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-radius: 5px;
                        border: 1px solid #ccc;
                    }
                    .btn-new {
                        width: 60px;
                        height: 35px;
                        border-radius: 10px;
                        color: white;
                        transition: .2s linear;
                        background: #0B63F6;
                    }
                    .btn-new:hover {
                        box-shadow: 0 0 0 2px white, 0 0 0 4px #3C82F8;
                    }
                </style>
            </head>
            <body>
		        <form method="post" action="/login" accept-charset="UTF-8">
				    <div class="mainContainer">
						<label for="surname"></label>
						<input type="text" autocomplete="off" placeholder="Ââåäèòå ôàìèëèş" name="surname" required>
						<label for="password"></label>
                        <input type="password" autocomplete="off" placeholder="Ïàğîëü àäìèíà" name="password" required>
						<button class="btn-new" type="submit">Âõîä</button>
				    </div>
		        </form>
            </body>
            </html>)#";

        res.set_content(page, "text/html");
    }

    if (req.method == "POST")
    {
        auto administrators = make_admins_list(users);

        const std::string correct_password = "15123415";

        auto surname = req.has_param("surname") ? req.get_param_value("surname") : "";
        auto password = req.has_param("password") ? req.get_param_value("password") : "";

        if (is_in_admins_list(surname, administrators) && password == correct_password)
        {
            Cookie cookie;
            cookie.name = "user_cookie";
            cookie.value = generateCookie(16);
            cookie.path = "/";
            cookie.maxAge = 3600;
            cookie.httpOnly = true;
            cookie.sameSite = Cookie::SameSiteLaxMode;

            sessions[cookie.value]["surname"] = surname;

            Cookie::set_cookie(res, cookie);

            std::cout << surname << " has been connected with cookie: " << cookie.value << std::endl;
        }

        res.set_redirect("/");
    }
}

void homeHandler(const Request& req, Response& res)
{
    auto cookie = Cookie::get_cookie(req, "user_cookie");
    auto& session = sessions[cookie.value];

    std::string page;

    if (req.method == "GET")
    {
        page += u8"<html>";
        page += u8"<header>";
        page += u8"<meta charset = 'utf-8'>";
        page += u8"<title>Administration page</title>";
        page += u8"<style>";
        page += u8"* {";
        page += u8"  font-family: Verdana, sans-serif;";
        page += u8"}";
        page += u8"table {";
        page += u8"  border: 1px solid #ddd;";
        page += u8"  border-collapse: collapse;";
        page += u8"  width: 50%;";
        page += u8"}";
        page += u8"th, td {";
        page += u8"  text-align: left;";
        page += u8"  border-bottom: 1px solid #ddd;";
        page += u8"}";
        page += u8"tr:hover {";
        page += u8"  background-color: #f5f5f5;";
        page += u8"}";
        page += u8".logout-button {";
        page += u8"  background-color: #4B535C;";
        page += u8"  color: white;";
        page += u8"  padding: 10px 20px;";
        page += u8"  border: none;";
        page += u8"  border-radius: 10px;";
        page += u8"  text-align: center;";
        page += u8"  text-decoration: none;";
        page += u8"  display: inline-block;";
        page += u8"  font-size: 16px;";
        page += u8"  margin: 4px 2px;";
        page += u8"  cursor: pointer;";
        page += u8"}";
        page += u8".delete-button {";
        page += u8"  background-color: #B30000;";
        page += u8"  color: white;";
        page += u8"  border: none;";
        page += u8"  border-radius: 10px";
        page += u8"  text-align: center;";
        page += u8"  text-decoration: none;";
        page += u8"  display: inline-block;";
        page += u8"  font-size: 12px;";
        page += u8"  cursor: pointer;";
        page += u8"}";
        page += u8".inp {";
        page += u8"  border: none;";
        page += u8"  background-color: #FFFFFF";
        page += u8"}";
        page += u8".frm {";
        page += u8"  width: auto;";
        page += u8"}";
        page += u8"</style>";
        page += u8"</header>";
        page += u8"<script>";
        page += u8"window.onload = function() {";
        page += u8"    var urlParams = new URLSearchParams(window.location.search);";
        page += u8"    if (urlParams.has('fileUploaded') && urlParams.get('fileUploaded') == 'true') {";
        page += u8"        alert('Ôàéë óñïåøíî çàãğóæåí!');";
        page += u8"    }";
        page += u8"};";
        page += u8"</script>";
        page += u8"<body><div><h1>Òàáëèöà ïîëüçîâàòåëåé</h1>";
        page += u8"<table><tr><td><strong>Ôàìèëèÿ</strong></td><td><strong>Ãğóïïà</strong></td><td><strong>Ğîëü</strong></td></tr>";

        for (const auto& user : users)
        {
            page += u8"<tr>";
            page += u8"<td>" + user.surname + "</td>";
            page += u8"<td>" + user.group + "</td>";
            page += u8"<td class='frm'>";
            page += u8"<form action='/update-role' method='post'>";
            page += u8"<input class='inp' type='text' name='position' value='" + user.position + "'>";
            page += u8"<input type='hidden' name='surname' value='" + user.surname + "'>";
            page += u8"</form>";
            page += u8"<form action='/delete-user' method='post'>";
            page += u8"<input type='hidden' name='surname' value='" + user.surname + "'>";
            page += u8"<button class='delete-button' type='submit'>Óäàëèòü</button>";
            page += u8"</form>";
            page += u8"</td></tr>";
        }

        page += u8"</table>";
        page += u8"<br><br>";
        page += u8"<form action='/logout' method='get'>";
        page += u8"<button class='logout-button' type='submit'>Âûõîä</button>";
        page += u8"</form>";
        page += u8"</div>";
        page += u8"<div>";
        page += u8"<form action='/upload-file' method='post' enctype='multipart/form-data'>";
        page += u8"<input type='file' name='file' accept='.xlsx'>";
        page += u8"<input type='submit'>";
        page += u8"</form>";
        page += u8"<form action='/send-file' method='post'>";
        page += u8"<button type='sumbit'>Îòïğàâèòü äàííûå</button>";
        page += u8"</form>";
        page += u8"</div>";
        page += u8"</body>";
        page += u8"</html>";

        res.set_content(page, "text/html");
    }
}

void logoutHandler(const Request& req, Response& res)
{
    if (req.method == "GET")
    {
        auto cookie = Cookie::get_cookie(req, "user_cookie");

        std::cout << "Cookie: " << cookie.value << " now is outdated." << std::endl;

        sessions.erase(cookie.value);

        Cookie new_cookie;
        new_cookie.name = "user_cookie";
        new_cookie.value = "";
        new_cookie.maxAge = -1;

        Cookie::set_cookie(res, new_cookie);

        res.set_redirect("/login");
    }
}

void updateRoleHandler(const Request& req, Response& res)
{
    std::string surname = req.get_param_value("surname");
    std::string newRole = req.get_param_value("position");

    for (auto& user : users)
    {
        if (user.surname == surname)
        {
            user.position = newRole;
            break;
        }
    }

    bsoncxx::builder::stream::document filter_builder{};
    filter_builder << "surname" << surname;

    bsoncxx::builder::stream::document update_builder{};
    update_builder << "$set" << bsoncxx::builder::stream::open_document
        << "position" << newRole
        << bsoncxx::builder::stream::close_document;

    collection.update_one(filter_builder.view(), update_builder.view());

    res.status = 200;
    res.set_redirect("/");
}

void deleteUserFromVector(const std::string& surname)
{
    users.erase(std::remove_if(users.begin(), users.end(),
        [&surname](const User& user) { return user.surname == surname; }), users.end());
}

void deleteUserHandler(const Request& req, Response& res)
{
    if (req.method == "POST")
    {
        std::string surname = req.get_param_value("surname");

        document builder{};
        builder << "surname" << surname;

        bsoncxx::stdx::optional<mongocxx::result::delete_result> is_deleted = collection.delete_one(builder.view());

        if (is_deleted)
        {
            deleteUserFromVector(surname);
            std::cout << "User " + surname + " is successfully deleted!" << std::endl;
        }
        else
        {
            std::cout << "An error occured while deleting a user..." << std::endl;
        }

        res.status = 200;
        res.set_redirect("/");
    }
}

void send_file_to_server(const std::string& server_path, const std::string& file_path)
{
    httplib::Client client("192.168.253.55", 8060);

    std::ifstream input_file(file_path, std::ios::binary);
    std::vector<char> file_data((std::istreambuf_iterator<char>(input_file)), std::istreambuf_iterator<char>());

    httplib::MultipartFormDataItems items =
    {
        { "file", file_data.data(), file_path, "application/octet-stream" },
    };

    auto result = client.Post(server_path.c_str(), items);

    if (result && result->status == 200)
    {
        std::cout << "File sent successfully\n";
    }
    else
    {
        std::cout << "Failed to send file\n";
    }
}

void uploadFileHandler(const Request& req, Response& res)
{
    if (req.method == "POST")
    {
        bool is_file_uploaded = req.has_file("file");

        if (is_file_uploaded)
        {
            std::cout << "Someone just uploaded a file!" << std::endl;
        }
        else
        {
            std::cout << "An error occured while uploading a file...";
            return;
        }

        const auto& file = req.get_file_value("file");
        std::string upload_directory = "C:\\Users\\maxim\\PycharmProjects\\excel_parser";
        std::string path = upload_directory + "\\schedule.xlsx";

        std::ofstream ofs(path, std::ios::binary);
        ofs << file.content;

        _chdir("C:\\Users\\maxim\\PycharmProjects\\excel_parser\\");
        system("start main.exe");

        res.set_redirect("/");
    }
}

void sendFileHandler(const Request& req, Response& res)
{
    if (req.method == "POST")
    {
        send_file_to_server("/upload", "C:\\Users\\maxim\\PycharmProjects\\excel_parser\\output.json");
        res.set_redirect("/");
    }
}