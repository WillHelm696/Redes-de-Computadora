//Tipos de datos que suma dos datos

#include<iostream>

using namespace std;

int main(){
    /*
    int num = 15;
    float ent = 15.50;
    double irs = 16.22323;
    bool Flag=true;
    char letra = 'a'; 
    | or binario
    && and logico 
    || or logico 
    */

    int numero1;
    int numero2;
    cout << "ingrese dos numeros mayores a 10 "<<endl;
    cin >> numero1 ;
    cin >> numero2 ;
    if (numero1>10 && numero2>10){
        cout<<"la suma es";
        return numero1+numero2;
    }
    else{
        cout <<"Los numeros no son  mayores a 10"<<endl;
    }
    return 0;
}