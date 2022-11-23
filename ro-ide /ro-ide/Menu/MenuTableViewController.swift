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
    res = fib(10);
    print(res);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Fibonacci - Iterativo", code: """
program fibonacciIter;

int n, f[9], res;

func int fibonacci(int n){
    int cont;
    print(1);
    cont = 2;
    while(cont < n){
        f[cont] = f[cont-1] + f[cont-2];
        cont = cont + 1;
    }
    return f[9];
}

main {
    f[0] = 0;
    f[1] = 1;
    res = fibonacci(9);
    print(res);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Factorial - Recursivo", code: """
program factorialRec;

int a, b, c;

func int factorial(int n){
    int res;
    print(n);
    if(n==0){
        res = 1;
    } else{
        res = factorial(n-1) * n;
    }
    return res;
}

main {
    a = 2;
    b = 600;
    c = factorial(7);
    print(c);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Factorial - Iterativo", code: """
program factorialIter;

int n, fun;

func int factorial(int n){
    int res, cont;
    print(1);
    cont = 2;
    res = 1;
    while(cont < n){
        res = res * cont;
        cont = cont + 1;
    }
    return res;
}

main {
    n = 5;
    fun = factorial(10);
    print(fun);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Find", code: """
program linearSearch;

int x, arr[10], size;

func void search(int n, int x){
    int i;
    print(1);
    i = 0;
    while(i < n){
        if (arr[i] == x){
            print(i);
        }
        i = i + 1;
    }
    return;
}

main{
    arr[0] = 2;
    arr[1] = 3;
    arr[2] = 4;
    arr[3] = 10;
    arr[4] = 40;
    x = 4;
    size = 5;
    search(size,x);
}
""", canEdit: false))
    dataSource.append(ProgramTest(title: "Sort", code: """
program bubbleSort;

int n, arr[10], f;

func void bubblesort(int n){
   int i, j, aux;
   print(1);
   arr[0] = 3;
   arr[1] = 2;
   arr[2] = 4;
   arr[3] = 8;
   arr[4] = 9;
   arr[5] = 4;
   arr[6] = 24;
   arr[7] = 12;
   arr[8] = 11;
   arr[9] = 32;
   i = 0;
   j = 0;
   while(i < n-1){
    j = 0;
    while(j < n-i-1){
        if (arr[j] > arr[j+1]){
            aux = arr[j+1];
            arr[j+1] = arr[j];
            arr[j] = aux;
        }
       j = j + 1;
    }
    i = i + 1;
   }
   return;
}

func void imprimir(int n){
    int i;
    print(1);
    i = 0;
    while(i < n){
        print(arr[i]);
        i = i + 1;
    }
    return;
}

main {
    n = 9;
    bubblesort(n);
    imprimir(n);
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
