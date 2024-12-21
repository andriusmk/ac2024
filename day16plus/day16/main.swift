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

struct Way {
    let state: State
    let cost: Int
}

func findExits(fromState state: State, in maze: Maze) -> [Way] {
    let testWays = [
        Way(state: state, cost: 0),
        Way(state: State(pos: state.pos, dir: state.dir.rotatedCCW), cost: 1000),
        Way(state: State(pos: state.pos, dir: state.dir.rotatedCW), cost: 1000)
    ]
    
    return testWays.filter({maze.isWalkable($0.state.pos + $0.state.dir)})
}

func findExits(fromWay way: Way, in maze: Maze) -> [Way] {
    return findExits(fromState: way.state, in: maze).map{Way(state: $0.state, cost: $0.cost + way.cost)}
}

func findNeighbour(maze: Maze, start: Way) -> Way? {
    var state = start.state
    var cost = start.cost
    
    while true {
        state = State(pos: state.pos + state.dir, dir: state.dir)
        cost += 1
        
        if state.pos == maze.finish {
            return Way(state: state, cost: cost)
        }
        
        let exits = findExits(fromState: state, in: maze)
        if exits.isEmpty {
            return nil
        }
        if exits.count > 1 {
            return Way(state: state, cost: cost)
        }
        
        let wayToGo = exits[0]
        state = wayToGo.state
        cost += wayToGo.cost
    }
}

func findCheapestPath(maze: Maze) -> Int? {
    var visited = Set<State>()
    var nodeCost = Dictionary<State, Int>()
    let initialState = State(pos: maze.start, dir: Vector2D(1, 0))
    var cheapestWay = Way(state: initialState, cost: 0)
    nodeCost[cheapestWay.state] = 0
    
    func updateNeighbours(of node: Way) {
        let exits = findExits(fromWay: node, in: maze)
        for ex in exits {
            if let neighbour = findNeighbour(maze: maze, start: ex) {
                if visited.contains(neighbour.state) == false {
                    let cost = nodeCost[neighbour.state] ?? neighbour.cost
                    nodeCost[neighbour.state] = min(cost, neighbour.cost)
                }
            }
        }
    }
    func findCheapestWay() -> Way? {
        var result: Way?
        for (state, cost) in nodeCost {
            if result == nil || cost < result!.cost {
                result = Way(state: state, cost: cost)
            }
        }
        return result
    }
    
    while true {
        let currentState = cheapestWay.state
//        print("pos:\(currentState.pos.x),\(currentState.pos.y) " +
//              "dir:\(currentState.dir.x),\(currentState.dir.y) " +
//              "dist:\(cheapestWay.cost)")
        if currentState.pos == maze.finish {
            break
        }
        updateNeighbours(of: cheapestWay)
        visited.insert(currentState)
        nodeCost.removeValue(forKey: currentState)
        
        guard let newCheapestWay = findCheapestWay() else {return nil}
        
        cheapestWay = newCheapestWay
    }
    
    return cheapestWay.cost
}


print(findCheapestPath(maze: parse(try String(contentsOfFile: "input", encoding: .ascii))!) ?? -1)
