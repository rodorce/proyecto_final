//
//  MenuTableViewController.swift
//  ro-ide
//
//  Created by Rodolfo Ramirez on 21/11/22.
//

import UIKit

class MenuTableViewController: UITableViewController {

  var dataSource: [ProgramTest] = []
  
  override func viewDidLoad() {
    super.viewDidLoad()
    self.navigationItem.title = "RO Compiler 🐍🐍🐍"
    fillDataSource()
    registerCells()
  }

  private func registerCells() {
    self.tableView.register(UITableViewCell.self, forCellReuseIdentifier: "defaultCell")
  }

  private func fillDataSource() {
    dataSource.append(ProgramTest(title: "Fibonacci - Recursivo", code: """
program fibonacciRec;

int res;

func int fib(int n){
    int resLocal1;
    int resLocal2;
    print(1);
    if (n < 1){
        resLocal2 = n;
    }else {
       resLocal1 = fib(n-1);
       resLocal2 = fib(n-2) + resLocal1;
    }
    return resLocal2;
}

main {
    res = fib(3);
    print(res);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Fibonacci - Iterativo", code: """
program programa4;

int n, cont, f[9];
main {
n = 9;
cont = 2;
f[0] = 0;
f[1] = 1;
while(cont < n+1){
    f[cont] = f[cont-1] + f[cont-2];
    print(cont);
    cont = cont+1;
}
print(f[9]);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Factorial - Recurisvo", code: """
program programita3;

int a, b, c;

func int factorial(int n){
    int res;
    print(n);
    print(n);
    if(n==0){
        print(n);
        res = 1;
    } else{
        res = factorial(n-1) * n;
    }
    return res;
}

main {
    a = 2;
    b = 600;
    c = factorial(10);
    print(c);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Factorial - Iterativo", code: """
Aqui
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Find", code: """
Aqui
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Sort", code: """
program bubbleSort;

int n, cont1, cont2, aux, printCont, f[9];
main {
n = 9;
f[0] = 0;
f[1] = 1;
f[2] = 4;
f[3] = 2;
f[4] = 10;
f[5] = 7;
f[6] = 5;
f[7] = 9;
f[8] = 14;
cont1 = 0;
cont2 = 0;
printCont = 0;
while(cont1 < n-1){
    cont2 = 0;
    while(cont2 < n-cont1-2){
        if(f[cont2] > f[cont2 + 1]){
            aux = f[cont2 + 1];
            f[cont2 + 1] = f[cont2];
            f[cont2] = aux;
        }
        cont2 = cont2 + 1;
    }
    cont1 = cont1 + 1;

}

while(printCont < 8){
    print(f[printCont]);
    printCont = printCont + 1;
}
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Otro", code: "", canEdit: true))
  }
  
  // MARK: - Table view data source
  
  override func numberOfSections(in tableView: UITableView) -> Int {
    return 1
  }
  
  override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
    return dataSource.count
  }
  
  override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
    let cell = tableView.dequeueReusableCell(withIdentifier: "defaultCell", for: indexPath)

    cell.textLabel?.text = dataSource[indexPath.row].title
    cell.selectionStyle = .none
    
    return cell
  }
  
  override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
    let vc: CompilerViewController = CompilerViewController.makeCompilerVC(model: dataSource[indexPath.row])
    self.navigationController?.pushViewController(vc, animated: true)
  }
  
}
