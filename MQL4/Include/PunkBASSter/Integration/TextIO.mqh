#include "DataContracts.mqh"
#include <Files\FilePipe.mqh>

class CTextIO
{
private:
   CFilePipe _filePipe;

public:
   void Open(string name)
   {
      int handle = _filePipe.Open(name, FILE_READ|FILE_WRITE|FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_ANSI);
      if (handle==INVALID_HANDLE)
      {
         Print("Invalid file/pipe handle!");
      }
   }
   
   string ExportDataGetTrade(string exportedString)
   {
      _filePipe.WriteString(exportedString,StringLen(exportedString));
      
      bool hasData = _filePipe.WaitForRead(1);
      
      //string result;
      //_filePipe.ReadString(result,File);
      char arr[];
      _filePipe.ReadArray(arr);
      //return result;
      return CharArrayToString(arr);
   }
   
   string ExportDataGetTrade(string const &exportedStrings[])
   {
      int size = ArraySize(exportedStrings);
      string responses[];
      ArrayResize(responses,size);
      
      //_filePipe.WriteArray(exportedStrings);
      for (int i=0; i<size; i++)
      {
         _filePipe.WriteString(exportedStrings[i],StringLen(exportedStrings[i]));
         bool read =_filePipe.ReadString(responses[i],1);
      }   
      
      string result;
      _filePipe.ReadString(result);
      return result;
   }
   
   void Close()
   {
      _filePipe.Close();
   }
};


/*
#include <Object.mqh>

//--- input parameters
input string   IndicatorPath = "MyIndicators\\ZigZag\\DZZ_Percent.ex5";
input string   OutputFileNameBase = "Dzz";

input double   InpPercent = 0.3;
input double   InpLevels = 1;
input bool     SortByAscendingDate = true;

void OnStart()
{
   string sym = Symbol();
   ENUM_TIMEFRAMES tf = Period();
   
   int hZz = iCustom(sym,tf,IndicatorPath,InpPercent,InpLevels);
   
   int barsCount = Bars(sym,tf);
   datetime time[];
   double zzTop[];
   double zzBot[];
   
   ArraySetAsSeries(time, !SortByAscendingDate);
   ArraySetAsSeries(zzTop, !SortByAscendingDate);
   ArraySetAsSeries(zzBot, !SortByAscendingDate);
   
   int total = CopyTime(sym,tf,0,barsCount,time);
   total = MathMin(CopyBuffer(hZz,1,0,barsCount,zzTop),total);
   total = MathMin(CopyBuffer(hZz,0,0,barsCount,zzBot),total);
      
   int fileHandle = OpenFile();
   
   FileWriteString(fileHandle, "Timestamp,Value\n");
   
   for(int i=0; i<=total-1; i++)
   {
      if(zzTop[i] > 0 && zzTop[i]!=EMPTY_VALUE)
      {
         string str = StringFormat("%d,%f\r\n", GetTimeStamp(time[i]), zzTop[i]);
         FileWriteString(fileHandle,str);
         continue;
      }
      
      if(zzBot[i] > 0 && zzBot[i]!=EMPTY_VALUE)
      {
         string str = StringFormat("%d,%f\r\n", GetTimeStamp(time[i]), zzBot[i]);
         FileWriteString(fileHandle,str);
         continue;
      }
   }

   FileClose(fileHandle);
}

int OpenFile()
{
   return FileOpen(GetFileName(),FILE_WRITE|FILE_COMMON|FILE_ANSI);
}

long GetTimeStamp(datetime dateTime)
{
   return IntegerToString(dateTime);
}

string GetFileName()
{
   return OutputFileNameBase + "_" + Symbol() + "_" + EnumToString(Period()) + ".csv";
}

*/