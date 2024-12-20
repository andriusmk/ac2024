//
//  main.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 19/12/2024.
//

import Foundation

struct State : Hashable {
    let pos: Vector2D
    let dir: Vector2D
    var ahead: (State, Int) {
        (State(pos: pos + dir, dir: dir), 1)
    }
    var left: (State, Int) {
        let newDir = dir.rotatedCCW
        return (State(pos: pos + newDir, dir: newDir), 1001)
    }
    var right: (State, Int) {
        let newDir = dir.rotatedCW
        return (State(pos: pos + newDir, dir: newDir), 1001)
    }
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
            fallthrough
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

func findNeighbour(maze: Maze, node: State) -> (State, Int)? {
    var state = node
    var cost = 0
    while true {
        let next_states = [state.ahead, state.left, state.right].filter{maze.isWalkable($0.0.pos)}
        
        if next_states.isEmpty {
            return nil
        }
        
        if next_states.count > 1 {
            return (state, cost)
        }
        // Not a dead end, not a node
        let (newState, newCost) = next_states[0]
        state = newState
        cost += newCost
        
        if state.pos == maze.finish {
            return (state, cost)
        }
    }
}

func findCheapestPath(maze: Maze) -> Int? {
    var visited = Set<State>()
    var nodeCost = Dictionary<State, Int>()
    var result: Int?
    func visit(node: State) {
        if visited.contains(node) {
            return
        }
        visited.insert(node)
        let cost = nodeCost[node]!
        if node.pos == maze.finish {
            let res = result ?? cost
            result = min(res, cost)
            return
        }
        let nextSteps = [node.ahead, node.left, node.right].filter({maze.isWalkable($0.0.pos)})
        let neighbours: [(State, Int)] = nextSteps.map({(step, initialCost) in
            guard let (neighbour, cost) = findNeighbour(maze: maze, node: step) else {return nil}
            return (neighbour, initialCost + cost)
        }).filter({$0 != nil}).map({$0!})
        for (neighbour, relCost) in neighbours {
            let absCost = cost + relCost
            let storedCost = nodeCost[neighbour] ?? absCost
            nodeCost[neighbour] = min(absCost, storedCost)
        }
        for neighbour in neighbours.map({$0.0}).sorted(by: {nodeCost[$0]! < nodeCost[$1]!}) {
            visit(node: neighbour)
        }
    }
    let initialState = State(pos: maze.start, dir: Vector2D(1, 0))
    nodeCost[initialState] = 0
    visit(node: initialState)
    
    return result
}


print(findCheapestPath(maze: parse(try String(contentsOfFile: "input", encoding: .ascii))!) ?? -1)
