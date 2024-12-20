//
//  utils.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 19/12/2024.
//
import Foundation

struct Vector2D : Hashable {
    let x: Int
    let y: Int
    
    init(_ x: Int, _ y: Int) {
        self.x = x
        self.y = y
    }
}

func +(_ v1: Vector2D, _ v2: Vector2D) -> Vector2D {
    return Vector2D(v1.x + v2.x, v1.y + v2.y)
}

func scan2d(_ data: String, with function: (Int, Int, Character) -> Void) {
    for (y, line) in data.split(whereSeparator: \.isNewline).enumerated() {
        for (x, c) in line.enumerated() {
            function(x, y, c)
        }
    }
}
