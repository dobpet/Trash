using MoveControl;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace MoveControl.Model
{
    public sealed class GlobalModel : INotifyPropertyChanged
    {
        private static readonly GlobalModel instance = new GlobalModel();
        public static GlobalModel Instance
        {
            get
            {
                return instance;
            }
        }

        private Task sender;
        

        private GlobalModel()
        {
            sender = new Task(() =>
            {
                while (true) {
                    //SendTCPPacket("127.0.0.1", "BUZ:0:");
                    string msg = "CM1:";
                    msg = msg + LMotRequested.ToString() + ":" + RMotRequested.ToString();
                    msg = msg + ":" + Servo1.ToString() + ":0:0:0";
                    //SendTCPPacket("127.0.0.1", msg);
                    SendTCPPacket(IP_Destination, msg);
                    Thread.Sleep(1000);
                }
            });

            sender.Start();
        }

        private void SendUDTPacket()
        {
            Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

            IPAddress serverAddr = IPAddress.Parse("127.0.0.1");

            IPEndPoint endPoint = new IPEndPoint(serverAddr, 690);

            string text = "hello Hell!";

            byte[] send_buffer = Encoding.ASCII.GetBytes(text);
            sock.SendTo(send_buffer, endPoint);
        }
        private void SendTCPPacket(String server, String message)
        {

            Int32 port = 502;
            try
            {
                TcpClient client = new TcpClient(server, port);

                Byte[] data = System.Text.Encoding.ASCII.GetBytes(message);


                NetworkStream stream = client.GetStream();

            
                stream.Write(data, 0, data.Length);

                CommunicationPossible = "Communicated";
                CommunicationColor = Colors.Green;

                stream.Close();
                client.Close();
            }
            catch
            {
                CommunicationPossible = "Communication Error"; 
                CommunicationColor = Colors.Red;
            }


        }

        string _IP_Destination;
        public string IP_Destination
        { 
            get => _IP_Destination;
            set { SetProperty(ref _IP_Destination, value); }
        }

        string _communicationPossible;
        public string CommunicationPossible
        {
            get => _communicationPossible;
            set { SetProperty(ref _communicationPossible, value); }
        }

        Color _communicationColor;
        public Color CommunicationColor
        {
            get => _communicationColor;
            set { SetProperty(ref _communicationColor, value); }
        }

        private sbyte _ControllerX;
        public sbyte ControllerX
        {
            get => _ControllerX;
            set 
            { 
                SetProperty(ref _ControllerX, value);
                CalculateMotorPower();
            }
        }

        private sbyte _ControllerY;
        public sbyte ControllerY
        {
            get => _ControllerY;
            set
            {
                SetProperty(ref _ControllerY, value);
                CalculateMotorPower();
            }
        }

        private sbyte _Servo1;
        public sbyte Servo1
        {
            get => _Servo1;
            set
            {
                SetProperty(ref _Servo1, value);
            }
        }

        private sbyte _Servo2;
        public sbyte Servo2
        {
            get => _Servo2;
            set
            {
                SetProperty(ref _Servo2, value);
            }
        }

        private sbyte _LMotRequested;
        public sbyte LMotRequested
        {
            get => _LMotRequested;
            set
            {
                SetProperty(ref _LMotRequested, value);
                //CalculateMotorPower();
            }
        }

        private sbyte _RMotRequested;
        public sbyte RMotRequested
        {
            get => _RMotRequested;
            set
            {
                SetProperty(ref _RMotRequested, value);
                //CalculateMotorPower();
            }
        }

        private double Scale(int value, int min, int max, int minScale, int maxScale)
        {
            double scaled = minScale + (double)(value - min) / (max - min) * (maxScale - minScale);
            return scaled;
        }

        private void CalculateMotorPower()
        {
            //LMotRequested = ControllerX;
            //RMotRequested = ControllerY;
            sbyte x = (sbyte)(+1 * ControllerX);
            sbyte y = (sbyte)(-1 * ControllerY);

            double angle = 0;
            double radians = 0;
            double vector = 0;

            vector = Math.Sqrt( Math.Pow(x, 2) + Math.Pow(y,2));
            if (vector > 100) vector = 100;
            if (vector < -100) vector = -100;

            int ParthAngle = 0;
            int Maximum = 0;

            if (x != 0)
            {
                //alfa = Math.Tan(y / x);
                radians = Math.Atan2(y, x);
                angle = radians * (180 / Math.PI);
                if (angle < 0)
                {
                    angle = 180 + (180 + angle);
                }
            }
            else if (y > 0) angle = 90;
            else if (y < 0) angle = 270;

            ParthAngle = (int)(angle % 45);


            if (angle < 45)
            {
                
                LMotRequested = (sbyte)vector;
                Maximum = (int)Scale(ParthAngle, 0, 45, -100, 50);
                RMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum); // inX, inY, outX, outY
            }
            else if (angle < 90)
            {
                LMotRequested = (sbyte)vector;
                Maximum = (int)Scale(ParthAngle, 0, 45, 50, 100);
                RMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
            }
            else if (angle < 135)
            {
                RMotRequested = (sbyte)vector;
                Maximum = (int)Scale(ParthAngle, 0, 45, 100, 50);
                LMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
            }
            else if (angle < 180)
            {
                RMotRequested = (sbyte)vector;
                Maximum = (int)Scale(ParthAngle, 0, 45, 50, -100);
                LMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
            }
            else if (angle < 225)
            {
                Maximum = (int)Scale(ParthAngle, 0, 45, -100, -50);
                LMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
                Maximum = (int)Scale(ParthAngle, 0, 45, 100, -100);
                RMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
            }
            else if (angle < 270)
            {
                RMotRequested = (sbyte)((-1) * vector);
                Maximum = (int)Scale(ParthAngle, 0, 45, -50, -100);
                LMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
            }
            else if (angle < 315)
            {
                LMotRequested = (sbyte)((-1) * vector);
                Maximum = (int)Scale(ParthAngle, 0, 45, -100, -50);
                RMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
            }
            else if(angle < 360)
            {
                Maximum = (int)Scale(ParthAngle, 0, 45, -100, 100);
                LMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
                Maximum = (int)Scale(ParthAngle, 0, 45, -50, -100);
                RMotRequested = (sbyte)Scale((int)vector, 0, 100, 0, Maximum);
            }

        }


        bool SetProperty<T>(ref T storage, T value, [CallerMemberName] string propertyName = null)
        {
            if (Object.Equals(storage, value))
                return false;

            storage = value;
            OnPropertyChanged(propertyName);
            return true;
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
