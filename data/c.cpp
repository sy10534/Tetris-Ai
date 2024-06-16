#include<bits/stdc++.h>
using namespace std;
int main(){
    int n;
    cin >> n;
    vector<pair<int,int>> giant(n);
    int height = 0;
    long long head = 1e9;
    for(int i = 0; i < n; i++){
        long long a,b;
        cin >> a >> b;
        height+=a;
        head = max(head,b-a);
    }
    cout << height+head;
    
}