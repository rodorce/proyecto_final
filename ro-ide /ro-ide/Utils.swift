//
//  Utils.swift
//  ro-ide
//
//  Created by Rodolfo Ramirez on 21/11/22.
//

import Foundation
import UIKit

fileprivate var spinner: UIView?

extension UIViewController {

  func showSpinner() {
    spinner = UIView(frame: self.view.bounds)
    spinner?.backgroundColor = UIColor(red: 0.5, green: 0.5, blue: 0.5, alpha: 0.5)

    let activityIndicator: UIActivityIndicatorView = UIActivityIndicatorView(style: .large)
    activityIndicator.center = spinner!.center
    activityIndicator.startAnimating()
    spinner?.addSubview(activityIndicator)
    self.view.addSubview(spinner!)
  }

  func removeSpinner() {
    spinner?.removeFromSuperview()
    spinner = nil
  }
}
