// WebRequests.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include <string>
#include <windows.h>
#include <cpprest/http_client.h>
#include <cpprest/json.h>                       // JSON library



using namespace std;
using namespace utility;                    // Common utilities like string conversions
using namespace web;                        // Common features like URIs.
using namespace web::http;                  // Common HTTP functionality
using namespace web::http::client;          // HTTP client features
using namespace Concurrency::streams;


_DLLAPI int PostJsonRequest(wchar_t *url, wchar_t *req_body, wchar_t *out_resp_body)
{
	auto url_str = wstring(url);
	auto json = json::value::parse(wstring(req_body));
	
	http_client client(url_str);

	web::http::http_request postTestRequest(web::http::methods::POST);
	postTestRequest.set_body(json);

	http_response response = client.request(postTestRequest).get();

	if (response.status_code() == status_codes::OK)
	{
		auto response_body = response.extract_utf16string().get().c_str();
		
		memcpy(out_resp_body, response_body, wcslen(response_body)*sizeof(wchar_t));
	}

	return response.status_code();
}


_DLLAPI double PostJsonRequestDbl(wchar_t *url, wchar_t *req_body)
{
	auto url_str = wstring(url);
	auto json = json::value::parse(wstring(req_body));

	http_client client(url_str);

	web::http::http_request postTestRequest(web::http::methods::POST);
	postTestRequest.set_body(json);

	http_response response = client.request(postTestRequest).get();

	if (response.status_code() == status_codes::OK)
	{
		auto response_body = response.extract_utf16string().get();

		return stod(response_body);
	}

	return -1.;
}