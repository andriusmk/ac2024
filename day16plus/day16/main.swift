//
//  main.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 19/12/2024.
//

import Foundation

struct Maze {
    let walkable: Set<Vector2D>
    let start: Vector2D
    let finish: Vector2D
}

func parse(_ map: String) -> Maze? {
    var walkable = Set<Vector2D>()
    var start: Vector2D?
    var finish: Vector2D?
    
    scan2d(map) { (x, y, c) in
        switch c {
        case "S":
            start = Vector2D(x, y)
        case "E":
            finish = Vector2D(x, y)
        case ".":
            walkable.insert(Vector2D(x, y))
        default:
            ()
        }
    }
    
    guard let start else { return nil }
    guard let finish else {return nil }

    return Maze(walkable: walkable, start: start, finish: finish)
}

print(parse("####\n#S.#\n#.E#\n####"))

