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
    let track: Set<Vector2D>
    
    func merge(with other: Way) -> Way {
        Way(target: target, distance: distance, track: track.union(other.track))
    }
}

func findExits(fromState state: State, in maze: Maze) -> [Way] {
    let testWays = [
        Way(target: state, distance: 0, track: [state.pos]),
        Way(target: State(pos: state.pos, dir: state.dir.rotatedCCW), distance: 1000, track: [state.pos]),
        Way(target: State(pos: state.pos, dir: state.dir.rotatedCW), distance: 1000, track: [state.pos])
    ]
    
    return testWays.filter({maze.isWalkable($0.target.pos + $0.target.dir)})
}

func findExits(fromWay way: Way, in maze: Maze) -> [Way] {
    return findExits(fromState: way.target, in: maze).map{Way(target: $0.target, distance: $0.distance + way.distance, track: way.track)}
}

func findNeighbour(maze: Maze, start: Way) -> Way? {
    var state = start.target
    var cost = start.distance
    var track: [Vector2D] = []
    
    while true {
        state = State(pos: state.pos + state.dir, dir: state.dir)
        cost += 1
        track.append(state.pos)
        
        let exits = findExits(fromState: state, in: maze)
        if exits.isEmpty {
            return nil
        }
        
        if exits.count > 1 || state.pos == maze.finish {
            return Way(target: state, distance: cost, track: start.track.union(track))
        }
        
        let wayToGo = exits[0]
        state = wayToGo.target
        cost += wayToGo.distance
    }
}

func findCheapestPath(maze: Maze) -> (Int, Int)? {
    let initialState = State(pos: maze.start, dir: Vector2D(1, 0))
    
    var visited = Set<State>()
    var heads = Dictionary<State, Way>()
    var cheapestWay = Way(target: initialState, distance: 0, track: [initialState.pos])
    heads[cheapestWay.target] = cheapestWay
    
    func updateNeighbours(of node: Way) {
        let exits = findExits(fromWay: node, in: maze)
        for ex in exits {
            if let neighbour = findNeighbour(maze: maze, start: ex) {
                if visited.contains(neighbour.target) == false {
                    let way = heads[neighbour.target]
                    if way == nil || way!.distance > neighbour.distance {
                        heads[neighbour.target] = neighbour
                    } else if way!.distance == neighbour.distance {
                        heads[neighbour.target] = Way(target: neighbour.target, distance: neighbour.distance, track: way!.track.union(neighbour.track))
                    }
                }
            }
        }
    }
    
    while cheapestWay.target.pos != maze.finish {
        let currentState = cheapestWay.target
        updateNeighbours(of: cheapestWay)
        visited.insert(currentState)
        heads.removeValue(forKey: currentState)
        
        guard let newCheapestWay = heads.values.min(by: {$0.distance < $1.distance})
        else {
            return nil
        }
        
        cheapestWay = newCheapestWay
    }
    
    return (cheapestWay.distance, cheapestWay.track.count)
}


print(findCheapestPath(maze: parse(try String(contentsOfFile: "input", encoding: .ascii))!) ?? (-1, -1))
