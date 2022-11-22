//
//  CompilerViewController.swift
//  ro-ide
//
//  Created by Rodolfo Ramirez on 21/11/22.
//

import UIKit

class CompilerViewController: UIViewController {

  static func makeCompilerVC(model: ProgramTest) -> CompilerViewController {
    let compilerVC: CompilerViewController = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "CompilerViewController") as! CompilerViewController
    compilerVC.model = model

    return compilerVC
  }

  @IBOutlet weak var inputTextView: UITextView!
  @IBOutlet weak var outputTextView: UITextView!

  private var model: ProgramTest!

  override func viewDidLoad() {
    super.viewDidLoad()
    setup()
  }

  private func setup() {
    self.navigationItem.title = model.title
    inputTextView.isEditable = model.canEdit
    inputTextView.text = model.code
    inputTextView.layer.borderWidth = 1
    inputTextView.layer.borderColor = UIColor.black.cgColor
    outputTextView.layer.borderWidth = 1
    outputTextView.layer.borderColor = UIColor.black.cgColor
    inputTextView.delegate = self
  }

  @IBAction func compile(_ sender: Any) {
    showSpinner()
    DispatchQueue.global().async {
      self.requestService()
    }
  }

  func requestService() {
    let params = ["code":model.code] as Dictionary<String, String>
    var request: URLRequest = URLRequest(url: URL(string: "http://127.0.0.1:5000/compile")!)
    request.httpMethod = "POST"
    request.httpBody = try? JSONSerialization.data(withJSONObject: params, options: [])
    request.addValue("application/json", forHTTPHeaderField: "Content-Type")

    let session = URLSession.shared
    let task = session.dataTask(with: request, completionHandler: { data, response, error -> Void in
        print(response!)
        do {
            let json = try JSONSerialization.jsonObject(with: data!) as! Dictionary<String, AnyObject>
            print(json)
          DispatchQueue.main.async {
            let newLine: String = self.outputTextView.text.isEmpty ? "" : "\n"
            self.outputTextView.text.append("\(newLine)\(json["response"] as! String)")
            self.removeSpinner()
          }
        } catch {
            print("error")
          self.removeSpinner()
        }
    })

    task.resume()
  }
}

extension CompilerViewController: UITextViewDelegate {

  func textViewDidChange(_ textView: UITextView) {
    model.code = textView.text
  }
}
