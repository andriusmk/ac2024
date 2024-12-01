//
//  main.swift
//  Day20
//
//  Created by Andrius Mazeikis on 03/01/2025.
//

import Foundation

func parse(_ data: String) -> Maze? {
    var start: Vector2D?
    var end: Vector2D?
    var obstacles = Set<Vector2D>()
    scan2d(data) { x, y, c in
        switch c {
        case "S":
            start = Vector2D(x, y)
        case "E":
            end = Vector2D(x, y)
        case "#":
            obstacles.insert(Vector2D(x, y))
        default:
            ()
        }
    }
    guard let start, let end else { return nil }
    return Maze(obstacles: obstacles, start: start, finish: end)
}

struct Processor {
    let maze: Maze
    let limits: [Int]
    let maxLimit: Int
    let minimum: Int
    let directions = [
        Vector2D(1, 0),
        Vector2D(-1, 0),
        Vector2D(0, 1),
        Vector2D(0, -1)
    ]
    var position: Vector2D
    var path: [Vector2D]
    var stats: [[Int: Int]]
    
    init?(_ maze: Maze, limits: [Int], minimum: Int) {
        if limits.isEmpty { return nil }
        self.maze = maze
        self.limits = limits
        self.minimum = minimum
        maxLimit = limits.max()!
        position = maze.start
        path = [maze.start]
        stats = Array(repeatElement([Int: Int](), count: limits.count))
    }
    
    static func distance(_ v1: Vector2D, _ v2: Vector2D) -> Int {
        let diff = v1 + (-v2)
        return abs(diff.x) + abs(diff.y)
    }
    
    mutating func findCheats() {
        for (i, pos) in path.enumerated() {
            let dist = Self.distance(position, pos)
            if dist > maxLimit { continue }
            let saving = path.count - i - dist
            if saving < minimum { continue }
            for (j, limit) in limits.enumerated() {
                if dist <= limit {
                    stats[j][saving, default: 0] += 1
                }
            }
        }
    }
    
    mutating func process(_ data: String) {
        var lastPosition: Vector2D?
        while let newPos = directions.map({position + $0})
                .first(where: {$0 != lastPosition && maze.isWalkable($0) }) {
            lastPosition = position
            position = newPos
            findCheats()
            if position == maze.finish { break }
            path.append(position)
        }
    }
}

let data = try String(contentsOfFile: "input", encoding: .ascii)
if let maze = parse(data),
   var processor = Processor(maze, limits: [2, 20], minimum: 100) {
    processor.process(data)
    let result1 = processor.stats[0].values.reduce(0, (+))
    let result2 = processor.stats[1].values.reduce(0, (+))
    print(result1, result2)
}
