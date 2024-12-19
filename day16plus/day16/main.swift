//
//  main.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 19/12/2024.
//

import Foundation

func parse(map: String) -> [String] {
    return map.split(whereSeparator: \.isNewline).map{ String($0) }
}

print("Hello, this is day\(16)")

