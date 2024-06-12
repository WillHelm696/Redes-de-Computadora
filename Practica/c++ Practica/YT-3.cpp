//La sentencia switch

#include <iostream>
using namespace std;

int main(){
    int num;
    cout<<"Ingrese un numero del 1 al 100"<<endl;
    cin >> num;

    switch(num){
        case 1: 
            cout<<"esta en el rango de 1 a 10"<<endl; 
            break;
        case 2: 
            cout<<"esta en el rango de 11 a 20"<<endl;
            break;
        case 3: 
            cout<<"esta en el rango de 21 a 30"<<endl;
            break;
        case 4: 
            cout<<"esta en el rango de 31 a 40"<<endl;
            break;
        case 5: 
            cout<<"esta en el rango de 41 a 50"<<endl;
            break;
        case 6: 
            cout<<"esta en el rango de 51 a 60"<<endl;
            break;
        case 7: 
            cout<<"esta en el rango de 61 a 70"<<endl;
            break;
        case 8: 
            cout<<"esta en el rango de 71 a 80"<<endl;
            break;
        case 9: 
            cout<<"esta en el rango de 81 a 90"<<endl;
            break;
        case 10: 
            cout<<"esta en el rango de 91 a 100"<<endl;
            break;
    }

    return 0;
} 
