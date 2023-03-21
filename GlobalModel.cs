using MoveControl;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
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
                Thread.Sleep(100);
            });

            sender.Start();
        }

        

        bool communicationPossible;
        public bool CommunicationPossible
        {
            get => communicationPossible;
            set { SetProperty(ref communicationPossible, value); }
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
                LMotRequested = 3;
                RMotRequested = 3;
            }
            else if (angle < 180)
            {
                LMotRequested = 4;
                RMotRequested = 4;
            }
            else if (angle < 225)
            {
                LMotRequested = 5;
                RMotRequested = 5;
            }
            else if (angle < 270)
            {
                LMotRequested = 6;
                RMotRequested = 6;
            }
            else if (angle < 315)
            {
                LMotRequested = 7;
                RMotRequested = 7;
            }
            else if(angle < 360)
            {
                LMotRequested = 8;
                RMotRequested = 8;
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
