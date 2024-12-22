//
//  main.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 19/12/2024.
//

import Foundation

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
    
    if let start, let finish {
        return Maze(walkable: walkable, start: start, finish: finish)
    }
    
    return nil
}

struct State : Hashable {
    let pos: Vector2D
    let dir: Vector2D
}

struct Way {
    let state: State
    let cost: Int
    let track: Set<Vector2D>
}

func findExits(fromState state: State, in maze: Maze) -> [Way] {
    let testWays = [
        Way(state: state, cost: 0, track: [state.pos]),
        Way(state: State(pos: state.pos, dir: state.dir.rotatedCCW), cost: 1000, track: [state.pos]),
        Way(state: State(pos: state.pos, dir: state.dir.rotatedCW), cost: 1000, track: [state.pos])
    ]
    
    return testWays.filter({maze.isWalkable($0.state.pos + $0.state.dir)})
}

func findExits(fromWay way: Way, in maze: Maze) -> [Way] {
    return findExits(fromState: way.state, in: maze).map{Way(state: $0.state, cost: $0.cost + way.cost, track: way.track)}
}

func findNeighbour(maze: Maze, start: Way) -> Way? {
    var state = start.state
    var cost = start.cost
    var track: [Vector2D] = []
    
    func makeWay() -> Way {
        Way(state: state, cost: cost, track: start.track.union(track))
    }
    
    while true {
        state = State(pos: state.pos + state.dir, dir: state.dir)
        cost += 1
        track.append(state.pos)
        
        if state.pos == maze.finish {
            return makeWay()
        }
        
        let exits = findExits(fromState: state, in: maze)
        if exits.isEmpty {
            return nil
        }
        
        if exits.count > 1 {
            return makeWay()
        }
        
        let wayToGo = exits[0]
        state = wayToGo.state
        cost += wayToGo.cost
    }
}

func findCheapestPath(maze: Maze) -> (Int, Int)? {
    var visited = Set<State>()
    var heads = Dictionary<State, Way>()
    let initialState = State(pos: maze.start, dir: Vector2D(1, 0))
    var cheapestWay = Way(state: initialState, cost: 0, track: [initialState.pos])
    heads[cheapestWay.state] = cheapestWay
    
    func updateNeighbours(of node: Way) {
        let exits = findExits(fromWay: node, in: maze)
        for ex in exits {
            if let neighbour = findNeighbour(maze: maze, start: ex) {
                if visited.contains(neighbour.state) == false {
                    let way = heads[neighbour.state]
                    if way == nil || way!.cost > neighbour.cost {
                        heads[neighbour.state] = neighbour
                    } else if way!.cost == neighbour.cost {
                        heads[neighbour.state] = Way(state: neighbour.state, cost: neighbour.cost, track: way!.track.union(neighbour.track))
                    }
                }
            }
        }
    }
    
    while cheapestWay.state.pos != maze.finish {
        let currentState = cheapestWay.state
        updateNeighbours(of: cheapestWay)
        visited.insert(currentState)
        heads.removeValue(forKey: currentState)
        
        guard let newCheapestWay = heads.values.min(by: {$0.cost < $1.cost})
        else {
            return nil
        }
        
        cheapestWay = newCheapestWay
    }
    
    return (cheapestWay.cost, cheapestWay.track.count)
}


print(findCheapestPath(maze: parse(try String(contentsOfFile: "input", encoding: .ascii))!) ?? (-1, -1))
