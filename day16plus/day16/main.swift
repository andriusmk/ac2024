//
//  main.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 19/12/2024.
//

import Foundation

func parse(_ map: String) -> Maze? {
    var obstacles = Set<Vector2D>()
    var start: Vector2D?
    var finish: Vector2D?
    
    scan2d(map) { (x, y, c) in
        switch c {
        case "S":
            start = Vector2D(x, y)
        case "E":
            finish = Vector2D(x, y)
        case "#":
            obstacles.insert(Vector2D(x, y))
        default:
            ()
        }
    }
    
    if let start, let finish {
        return Maze(obstacles: obstacles, start: start, finish: finish)
    }
    
    return nil
}

struct State : Hashable {
    let pos: Vector2D
    let dir: Vector2D
}

struct Way : GraphEdge {
    let target: State
    let distance: Int
    let trace: Set<Vector2D>
    
}

struct Trace : GraphTrace {
    let trace: Set<Vector2D>
    func append(_ edge: Way) -> Trace {
        Trace(trace: trace.union(edge.trace))
    }
    func merge(with other: Trace) -> Trace {
        Trace(trace: trace.union(other.trace))
    }
}

extension Trace {
    init() {
        trace = []
    }
}

func findExits(fromState state: State, in maze: Maze) -> [Way] {
    let testWays = [
        Way(target: state, distance: 0, trace: [state.pos]),
        Way(target: State(pos: state.pos, dir: state.dir.rotatedCCW), distance: 1000, trace: [state.pos]),
        Way(target: State(pos: state.pos, dir: state.dir.rotatedCW), distance: 1000, trace: [state.pos])
    ]
    
    return testWays.filter({maze.isWalkable($0.target.pos + $0.target.dir)})
    
}

func findNeighbour(maze: Maze, start: Way) -> Way? {
    var state = start.target
    var cost = 0
    var trace = Set<Vector2D>([state.pos])
    
    while true {
        state = State(pos: state.pos + state.dir, dir: state.dir)
        cost += 1
        trace.insert(state.pos)
        
        let exits = findExits(fromState: state, in: maze)
        if exits.isEmpty {
            return nil
        }
        
        if exits.count > 1 || state.pos == maze.finish {
            return Way(target: state, distance: start.distance + cost, trace: trace)
        }
        
        let wayToGo = exits[0]
        state = wayToGo.target
        cost += wayToGo.distance
    }
}

func findNeighbours(maze: Maze, start: State) -> [Way] {
    let exits = findExits(fromState: start, in: maze)
    let result = exits.compactMap({ findNeighbour(maze: maze, start: $0 )})
    return result
}

func findCheapestPath(maze: Maze) -> (Int, Int)? {
    let initialState = State(pos: maze.start, dir: Vector2D(1, 0))
    if let (distance, trace): (Int, Trace) = dijkstra(
        with: { findNeighbours(maze: maze, start: $0)},
        start: initialState,
        isEnd: { $0.pos == maze.finish}) {
        
        return (distance, trace.trace.count)
    }
    return nil
}

if let result = findCheapestPath(maze: parse(try String(contentsOfFile: "input", encoding: .ascii))!) {
    print(result)
}
