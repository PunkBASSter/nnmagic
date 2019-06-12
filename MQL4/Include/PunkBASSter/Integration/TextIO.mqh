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
      char arr[];
      _filePipe.ReadArray(arr);
      return CharArrayToString(arr);
   }
   
   string ExportDataGetTrade(string const &exportedStrings[])
   {
      int size = ArraySize(exportedStrings);
      string responses[];
      ArrayResize(responses,size);

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