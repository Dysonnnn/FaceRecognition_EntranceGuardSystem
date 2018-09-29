/*参考  from  http://zhongbest.com/2017/06/14/手机通过esp8266控制arduino上的led灯at指令方式）/
*
*ESP8266 RX TX  接 arduino 右上角的TX  RX
*Arduino上再连接一个LED灯，程序中使用的是PIN11引脚。（连接LED灯需要在正极连接一个220欧姆的电阻）。
*/
 #include <Servo.h>
  int led_pin = 8;   
  char cmd[10];  //定义一个10字节的整型数据变量cmd作为命令，这里可以修改为不同的数字。此处设置为10是为了有更好的兼容性。
  bool valid_cmd = false;   //判断收到的cmd是否有内容
  Servo servo_0;
void servo_turn_clockwise()  //顺时针转180度
{
  int step;
  for (step = 0;step < 180;step ++)  //顺时针转180度
  {
    servo_0.write(step);
    delay(1);
    }
}

void servo_turn_anticlockwise()  //逆时针转180度
{
  int step;
  for (step = 180;step > 0;step --)  //逆时针转180度
  {
    servo_0.write(step);
    delay(1);
    }
}
void setup() 
{
  pinMode(led_pin, OUTPUT);  //定义连接led的引脚为输出信号
  Serial.begin(9600);
  servo_0.attach(3); //定义舵机口
}
void loop()
{   /*以下部分是串口信息处理过程*/

if (Serial.available() > 0) //如果串口收到有数据
{
  int i;//定义一个整数型变量i
  for (i = 0; i < 10; i++)//变量i最大为10
  {
    cmd[i] = '\0';//清空缓存，存入cmd变量，并以\0作为结束符
  }

  for (i = 0; i < 9; i++) //此时i只能取前9位，第10位是结束符\0
  { //再次判断串口如果收到有数据，防止数据丢失
    if (Serial.available() > 0)
    {
      cmd[i] = Serial.read();//给变量cmd赋值，取串口收到的前9位字符
      delay(1);
    } 
    else
    { 
      break;//如果串口数据超过9位，后面的字符直接忽略，跳到下一步
    }
  }
/*以上串口信息处理结束*/

valid_cmd = true;  //得到最终变量cmd的有效值
}
if (valid_cmd)  //判断变量cmd的值，开始处理
{
  if (0 == strncmp(cmd, "on", 2))  //如果变量cmd的前2位的值是on
  {
    digitalWrite(led_pin, HIGH);  //则连接led的引脚电压被置高5V，
    //驱动舵机
    servo_turn_clockwise();  //顺时针转180度
    Serial.println("ON:ready open the door");  //串口打印返回值ON，表示ON的操作执行成功
    delay(8000); //延时8秒
    servo_turn_anticlockwise();  //逆时针转180度，复位
    digitalWrite(led_pin, LOW);  //则连接继电器的引脚电压被置低0V，灯的电路被断开，灯灭
  }
  else if (0 == strncmp(cmd, "off", 3)) //否则如果变量cmd的前3位的值是off
  {
    digitalWrite(led_pin, LOW);  //则连接继电器的引脚电压被置低0V，灯的电路被断开，灯灭
   //舵机复位
    servo_turn_anticlockwise();  //逆时针转180度
    Serial.println("OFF"); //串口打印返回值F，表示OFF的操作执行成功
  }
  else //如果以上两个条件都不成立，前2位不是ON，或者前3位不是OFF，即不正确的命令
  {
    Serial.println("INPUT ERROR");//仅串口打印返回值X，表示指令错误。
  }
  //到此，变量cmd的指令被处理完毕
  valid_cmd = false;
}  
  //延迟10毫秒，返回loop主程序继续读取新的串口指令
  delay(10);
}

