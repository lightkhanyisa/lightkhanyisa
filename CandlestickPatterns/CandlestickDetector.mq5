//+------------------------------------------------------------------+
//|                                          CandlestickDetector.mq5 |
//|                                                      LightYagami |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "LightYagami"
#property link      "https://www.mql5.com"
#property version   "1.00"


int OnInit()
  {
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
    Doji();
    Engulfing();
    Hammer(0.07,0.07);
    Star(0.5);
   
  }
int Engulfing()
  {
   datetime time=iTime(_Symbol,PERIOD_CURRENT,1);
   double open=iOpen(_Symbol,PERIOD_CURRENT,1);
   double high=iHigh(_Symbol,PERIOD_CURRENT,1);
   double low=iLow(_Symbol,PERIOD_CURRENT,1);
   double close=iClose(_Symbol,PERIOD_CURRENT,1);
   double open2=iOpen(_Symbol,PERIOD_CURRENT,2);
   double high2=iHigh(_Symbol,PERIOD_CURRENT,2);
   double low2=iLow(_Symbol,PERIOD_CURRENT,2);
   double close2=iClose(_Symbol,PERIOD_CURRENT,2);
   if(open<close)
     {
      if(open2>close2)
        {
         if(high>high2&&low<low2)
           {
            if(close>open2&&open<close2)
              {
               createObj(time,low,217, clrGreen,"Bullish Engulfing");
                 {
                  return 1;
                 }
              }
           }
        }
     }
   if(open>close)
     {
      if(open2<close2)
        {
         if(high>high2&&low<low2)
           {
            if(close<open2&&open>close2)
              {
               createObj(time,high,218, clrRed,"Bearish Engulfing");
                 {
                  return -1;
                 }
              }
           }
        }
     }
   return 0;
  }
void createObj(datetime time, double price, int arrawCode, color clr, string txt)
  {
   string objName=" ";
   StringConcatenate(objName, "Signal at ",time, " at ",DoubleToString(price,_Digits)," (",arrawCode,")");
   if(ObjectCreate(0,objName,OBJ_ARROW,0,time,price))
     {
      ObjectSetInteger(0,objName,OBJPROP_ARROWCODE,arrawCode);
      ObjectSetInteger(0,objName,OBJPROP_COLOR,clr);
     }
   string candleName=objName+txt;
   if(ObjectCreate(0,candleName,OBJ_TEXT,0,time,price))
     {
      ObjectSetString(0,candleName,OBJPROP_TEXT," "+txt);
      ObjectSetInteger(0,candleName,OBJPROP_COLOR,clr);
     }
  }
int Doji()
  {
   datetime time=iTime(_Symbol,PERIOD_CURRENT,1);
   double open=iOpen(_Symbol,PERIOD_CURRENT,1);
   double high=iHigh(_Symbol,PERIOD_CURRENT,1);
   double low=iLow(_Symbol,PERIOD_CURRENT,1);
   double close=iClose(_Symbol,PERIOD_CURRENT,1);
//Doji
   if(open==close)
     {
      createObj(time,low,217, clrBlack,"Doji");
        {
         return 1;
        }
     }
   return 0;
  }
int Star(double middleCandleRatio)
  {
   datetime time=iTime(_Symbol,PERIOD_CURRENT,1);
   double open=iOpen(_Symbol,PERIOD_CURRENT,1);
   double high=iHigh(_Symbol,PERIOD_CURRENT,1);
   double low=iLow(_Symbol,PERIOD_CURRENT,1);
   double close=iClose(_Symbol,PERIOD_CURRENT,1);
   double open2=iOpen(_Symbol,PERIOD_CURRENT,2);
   double high2=iHigh(_Symbol,PERIOD_CURRENT,2);
   double low2=iLow(_Symbol,PERIOD_CURRENT,2);
   double close2=iClose(_Symbol,PERIOD_CURRENT,2);
   double open3=iOpen(_Symbol,PERIOD_CURRENT,3);
   double high3=iHigh(_Symbol,PERIOD_CURRENT,3);
   double low3=iLow(_Symbol,PERIOD_CURRENT,3);
   double close3=iClose(_Symbol,PERIOD_CURRENT,3);
   double candleSize=high-low;
   double candleSize2=high2-low2;
   double candleSize3=high3-low3;
   if(open<close)
     {
      if(open3>close3)
        {
         if(candleSize2<candleSize*middleCandleRatio && candleSize2<candleSize3*middleCandleRatio)
           {
            createObj(time,low,217, clrGreen,"Morning Star");
              {
               return 1;
              }
           }
        }
     }
   if(open>close)
     {
      if(open3<close3)
        {
         if(candleSize2<candleSize*middleCandleRatio && candleSize2<candleSize3*middleCandleRatio)
           {
            createObj(time,high,218, clrRed,"Evening Star");
              {
               return -1;
              }
           }
        }
     }
   return 0;
  }
int Hammer(double smallShadowRatio, double longShadowRatio)
  {
//creating variables for prices data - open,  high, low, close
   datetime time=iTime(_Symbol,PERIOD_CURRENT,1);
   double open=iOpen(_Symbol,PERIOD_CURRENT,1);
   double high=iHigh(_Symbol,PERIOD_CURRENT,1);
   double low=iLow(_Symbol,PERIOD_CURRENT,1);
   double close=iClose(_Symbol,PERIOD_CURRENT,1);
   double candleSize=high-low;   
//green hammer
   if(open<close)
     {
      if(high-close < candleSize*smallShadowRatio)
        {
         if(open-low>candleSize*longShadowRatio)
            createObj(time,low,217, clrGreen,"Hammer");
           {
            return 1;
           }
        }
     }
//red hammer
   if(open>close)
     {
      if(high-open<candleSize*smallShadowRatio)
        {
         if(close-low>candleSize*longShadowRatio)
            createObj(time,high,218,clrRed,"Hammer");
           {
            return 1;
           }
        }
     }
//green inverse hammer
   if(open<close)
     {
      if(open-low < candleSize*smallShadowRatio)
        {
         if(high-close>candleSize*longShadowRatio)
            createObj(time,low,217, clrGreen,"Inverted Hammer");
           {
            return -1;
           }
        }
     }
//red inverse hammer
   if(open>close)
     {
      if(close-low < candleSize*smallShadowRatio)
        {
         if(high-open>candleSize*longShadowRatio)
            createObj(time,high,218, clrRed,"Inverted Hammer");
           {
            return -1;
           }
        }
     }
   return 0;
  }