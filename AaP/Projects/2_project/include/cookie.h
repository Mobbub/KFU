#ifndef COOKIE_H
#define COOKIE_H

#include <vector>
#include <string>
#include <httplib.h>

using namespace httplib;

struct Cookie {
	/// �������� (����) cookie
	std::string name = "";
	/// �������� cookie
	std::string value = "";
	/// ������������� �����, ��� �������� ����� �������� cookie
	std::string domain = "";
	/// ������������� ���� �� �������, ��� �������� ����� �������� cookie
	std::string path = "";
	/// > 0 - ������������� ����������������� ����� �������� cookie � ��������; == 0 (�� ���������) - cookie ����� ���� �� ������� �������; < 0 - ������� ����������
	int maxAge = 0;
	/// ��������� ������ � cookie �� JavaScript, ��� �������� ������������� ����� �� ����� ������
	bool httpOnly = true;
	/// ���������, ��� cookie ������ ���� ��������� ������ �� ����������� (HTTPS) ����������
	bool secure = false;
	/// ���������, ��� cookie ������ ���� ��������� � ��������, ��������� � �����-��������� ���������
	std::string sameSite = SameSiteNoneMode;

	/// ���� ����������� �������� "Strict", cookie �� ����� ������������ � �����-�������� ��������. �� ����� ������������ ������ � ������, ���� ������� ���� ��������� � ������, �� ������� ���������� cookie
	static const std::string SameSiteStrictMode;
	/// ���� ����������� �������� "Lax", cookie ����� ������������ � �����-�������� ��������, ���� ��� "����������" HTTP-�����, ����� ��� GET, HEAD ��� OPTIONS, � ���� ��� �������� ������������ ������������� (��������, ������ �� ������). ������, ���� ������ ����������� �� �������, cookie �� ����� ������������
	static const std::string SameSiteLaxMode;
	/// ���� ����������� �������� "None", cookie ����� ������������ �� ���� �����-�������� ��������. ������ ��� ������������� ����� �������� ��������� ��������� �������� "Secure", ����� cookie ��� ������������ ������ �� ����������� (HTTPS) ����������
	static const std::string SameSiteNoneMode;

	/// Cookie -> string
	std::string to_string() const;
	/// ��������� HTTP ��������� � ������� ������ ������ ���������� cookie � ��������� ��� � ����� ������� res
	static void set_cookie(Response& res, const Cookie& cookie);
	/// �������� ����� � ������� req ���� � ������ name. ���� ����� ���, ������������ ������ ������, ���� name ���������� ������ ������ ����, �� ������ ������ ������� ������� ������
	static Cookie get_cookie(const Request& req, const std::string& name);
};

#endif // COOKIE_H