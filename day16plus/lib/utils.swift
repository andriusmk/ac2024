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
    var rotatedCW: Vector2D {
        Vector2D(-y, x)
    }
    var rotatedCCW: Vector2D {
        Vector2D(y, -x)
    }
    
    init(_ x: Int, _ y: Int) {
        self.x = x
        self.y = y
    }
}

func +(_ v1: Vector2D, _ v2: Vector2D) -> Vector2D {
    return Vector2D(v1.x + v2.x, v1.y + v2.y)
}

prefix func -(_ v: Vector2D) -> Vector2D {
    return Vector2D(-v.x, -v.y)
}

struct Maze {
    let obstacles: Set<Vector2D>
    let start: Vector2D
    let finish: Vector2D
    
    func isWalkable(_ pos: Vector2D) -> Bool {
        return obstacles.contains(pos) == false
    }
}

func scan2d(_ data: String, with function: (Int, Int, Character) -> Void) {
    for (y, line) in data.split(whereSeparator: \.isNewline).enumerated() {
        for (x, c) in line.enumerated() {
            function(x, y, c)
        }
    }
}

struct Pair<T1, T2> {
    let first: T1
    let second: T2
    init(_ first: T1, _ second: T2) {
        self.first = first
        self.second = second
    }
}

extension Pair: Equatable where T1: Equatable, T2: Equatable {
}

extension Pair: Hashable where T1: Hashable, T2: Hashable {
}

func pairwise<T>(_ src: some Sequence<T>) -> [Pair<T, T>] {
    return zip(src, src.dropFirst()).map{Pair($0.0, $0.1)}
}

func modInverse(a a0: Int, mod m0: Int) -> Int {
    var a = a0
    var mod = m0
    var y = 0
    var x = 1
    
    if mod == 1 {
        return 0
    }
    
    while a > 1 {
        let quot = a / mod
        (a, mod) = (mod, a % mod)
        (x, y) = (y, x - quot * y)
    }
    
    if x < 0 {
        x += m0
    }
    
    return x
}
