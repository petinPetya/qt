button_cap_style = """
  padding: 10px;
  background-color: #6f00ff;
  color: #fff;
  width: 8px;
  height: 6px;
  border: 1px solid black;
  border-radius: 1px;
  font-size: 16px;
  cursor: pointer;
  margin: 1px;
"""

button_cap_style_hover = """
  background-color: #722eb2;
  transform: translateY(-1px);
"""

text_style_title = """
  font: 3em Georgia, bold;
  color: #1d073d;
  background-color: #d3ccd8;
"""

container_style = """
  background-color: #ffffff;
  border: 1px solid #d0d0d0;
  border-radius: 3px;
"""

filter_button_style = """
  QPushButton {
      background-color: #6c757d;
      color: white;
      border: none;
      border-radius: 3px;
      font-size: 9px;
      font-weight: bold;
  }
  QPushButton:hover {
      background-color: #5a6268;
      border: 1px solid #545b62;
  }
  QPushButton:pressed {
      background-color: #545b62;
      padding: 1px 0px 0px 1px;
  }
"""


"""
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int MAXN = (int)1e5 + 7;
vector<vector<int>> g(MAXN, vector<int>(MAXN, 0));
vector<int> comp(MAXN);

void dfs(int v, int num) {
    comp[v] = num;
    for (int u : g[v]) {
        if (!comp[u]) {
            dfs(u, num);
        };
    };
};

int main() {
    int n, m;
    cin >> n >> m;
    while (m--) {
        int x, y;
        cin >> x >> y;
        g[x][y] = 1;
        g[y][x] = 1;
    }
    int num = 1;
    for (int v = 1; v < n + 1; v++) {
        if (!comp[v]) {
            dfs(v, num++);
        }
    }
    printf("%d\n", num);
    vector<vector<int>> res(num + 1, vector<int>());
    for (int i : comp) {
        printf("%d %d", i, comp[i]);
    }
    return 0;
}

"""
