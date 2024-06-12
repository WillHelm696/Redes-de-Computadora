// Algoritmo que decide el cuadrante que esta una cordenada
#include<iostream>
using namespace std;

int main(){
    
    int x1,y2;
    
    cout<<"Ingrese dos cordenadas polares"<<endl;
    cin>>x1>>y2;
    
    if (x1>0 && y2 > 0){
        cout<<"ESta en el primer cuadrante"<<endl;
    }    
    else if (x1 < 0 && y2 > 0){
        cout<<"ESta en el segundo cuadrante"<<endl;
    }
    else if (x1 < 0 && y2 < 0){
        cout<<"ESta en el Terser cuadrante"<<endl;
    }
    else if (x1 > 0 && y2 < 0){
        cout<<"ESta en el cuarto cuadrante"<<endl;
    }
    else if(x1==0 && y2 != 0){
        cout<<"Esta en el eje Y"<<endl;
    }
    else if(x1 != 0 && y2 == 0){
        cout<<"ESta en eeje X"<<endl;
    }
    else if(x1 == y2){
        cout<<"Esta en el origen de cordenadas"<<endl;
    }

return 0;
}
