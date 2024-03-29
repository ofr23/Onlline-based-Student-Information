#include <bits/stdc++.h>
using namespace std;
class graph{
    int v;
    vector<int> *adj;
    void DFSutil(int v, vector<bool> &visited){
        visited[v]=true;
        cout<<v<<" ";
        for(int i=0;i<v;i++){
            if(!visited[i])
                DFSutil(i,visited);
        }
    }
public:
    graph(int v){
        this->v = v;
        vector<int> adj[v];
    }
    void addEdge(int v,int w){
        adj[v].push_back(w);
    }
    void DFS(int source){
        vector<bool> visited;
        DFSutil(source, visited);
    }
};
int main()
{
    graph g(4);
    g.addEdge(0,1);
    g.addEdge(0,2);
    g.addEdge(1,2);
    g.addEdge(2,0);
    g.addEdge(2,3);
    g.addEdge(3,3);
    g.DFS(2);
    return 0;
}
