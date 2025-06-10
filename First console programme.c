#include <stdio.h>
#include <math.h>
#include <conio.h>
#include <Windows.h>
#include <stdlib.h>
#include <time.h>

void gotoxy(int x, int y)
{
    COORD c;
    c.X = x;
    c.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), c);
}

int main(void)
{
    srand(time(NULL));    
    HANDLE consoleHandler = GetStdHandle(STD_OUTPUT_HANDLE);

    double sum = 0;
    int textColor;
    int backgroundColor;
    long term = 1;
    long row = 0;

    while (!_kbhit())
    {
        double a = pow(-1, (term - 1)) / ((2 * term) - 1);
        textColor = rand() % 16;
        backgroundColor = rand() % 16;

        if(backgroundColor == textColor)
        {
            while(backgroundColor == textColor)
            {
                backgroundColor = rand() % 16;
            }
        }

        SetConsoleTextAttribute(consoleHandler, backgroundColor * 16 + textColor);
        gotoxy(0, row);

        if (a > 0)
        {
            printf(" %.6f\n", a);
        }
        else
        {
            printf("%.6f\n", a);
        }
        sum += a;
        SetConsoleTextAttribute(consoleHandler, 15);
        gotoxy(80, 10);
        printf("Suma: %.10f", sum);
        Sleep(500);
        term++;
        row++;

        if (row > 28)
        {
          row = 0;
          system("cls");
        }
    }
    return 0;
}