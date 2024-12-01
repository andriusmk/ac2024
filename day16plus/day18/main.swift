//
//  main.swift
//  day18
//
//  Created by Andrius Mazeikis on 28/12/2024.
//

import Foundation

enum CrawlerError: Error {
    case noRoute
}

struct FrameMaze {
    let size: Vector2D
    var obstacles: Set<Vector2D>
    
    func isWalkable(_ pos: Vector2D) -> Bool {
        return (0..<size.x).contains(pos.x) && (0..<size.y).contains(pos.y)
               && (obstacles.contains(pos) == false)
    }
}

func parse(_ data: String) -> [Vector2D] {
    let lines = data.split(whereSeparator: \.isNewline)
    let obstacles = lines.map({$0.split(separator: ",").compactMap({Int($0)})})
        .map({Vector2D($0[0], $0[1])})
    return obstacles
}


struct Crawler {
    var maze: FrameMaze
    let directions = [
        Vector2D(1, 0),
        Vector2D(-1, 0),
        Vector2D(0, 1),
        Vector2D(0, -1)
    ]
    let destination: Vector2D
    var distances = [Vector2D(0, 0): 0]
    var visited = Set<Vector2D>()
    
    init(_ maze: FrameMaze) {
        self.maze = maze
        self.destination = maze.size + Vector2D(-1, -1)
    }
    
    mutating func minDistance() -> Int? {
        while true {
            guard let (pos, dist) = distances.min(by: {$0.1 < $1.1}) else { return nil }
            if pos == destination {
                return dist
            }
            let testPoss = directions.map({$0 + pos}).filter({ maze.isWalkable($0)
                && !visited.contains($0)})
            for testPos in testPoss {
                if let testDist = distances[testPos] {
                    distances[testPos] = min(testDist, dist + 1)
                } else {
                    distances[testPos] = dist + 1
                }
            }
            visited.insert(pos)
            distances.removeValue(forKey: pos)
        }
    }

    mutating func reset() {
        distances.removeAll(keepingCapacity: true)
        distances[Vector2D(0, 0)] = 0
        visited.removeAll(keepingCapacity: true)
    }
}

let obstacles = parse(try String(contentsOfFile: "input", encoding: .ascii))
var maze = FrameMaze(size: Vector2D(71, 71), obstacles: Set(obstacles.prefix(1024)))

var crawler = Crawler(maze)
print(crawler.minDistance() ?? -1)

for obstacle in obstacles.dropFirst(1024) {
    crawler.reset()
    crawler.maze.obstacles.insert(obstacle)
    if crawler.minDistance() == nil {
        print([obstacle.x, obstacle.y].map({String($0)}).joined(separator: ","))
        break
    }
}
