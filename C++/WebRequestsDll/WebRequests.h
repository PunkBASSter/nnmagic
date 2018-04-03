#pragma once


__declspec(dllexport) double __stdcall __getMax(double* arr, const int size);
__declspec(dllexport) char* __stdcall __getForecast(char* url, char* payload);