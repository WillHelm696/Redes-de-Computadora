// Programa que calcula el factorial
#include<iostream>

using namespace std;

int main () {
    int num ;
    cout<<"Factorial de :"<<endl;
    cin>>num;
    int i = 0,fac = 1;
    while (i<num){
        fac += fac*i;
        i+=1;
    }
    cout<<num<<"!:"<<fac<<endl;
    return 0;

}