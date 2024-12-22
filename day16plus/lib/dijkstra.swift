//
//  dijkstra.swift
//  day16plus
//
//  Created by Andrius Mazeikis on 22/12/2024.
//

protocol GraphEdge {
    associatedtype Vertex : Hashable
    
    var distance: Int { get }
    var target: Vertex { get }
    func merge(with: Self) -> Self
}

func dijkstra<T : GraphEdge>(with getAdjacent: (T.Vertex) -> [T], start: T.Vertex, end: T.Vertex) -> Int? {
    var heads = Dictionary<T.Vertex, (T, Int)>()
    var current = start
    var currentDistance = 0
    var visited = Set<T.Vertex>()
    
    func updateAdjacent(_ edge: T) {
        let distance = currentDistance + edge.distance
        if let (storedEdge, storedDistance) = heads[edge.target] {
            if storedDistance > distance {
                heads[edge.target] = (edge, distance)
            } else if storedDistance == distance {
                heads[edge.target] = (edge.merge(with: storedEdge), distance)
            }
        } else {
            heads[edge.target] = (edge, distance)
        }
    }
    
    while current != start {
        for edge in getAdjacent(current).filter({!visited.contains($0.target)}) {
            updateAdjacent(edge)
        }
        visited.insert(current)
        heads.removeValue(forKey: current)
        guard let (leadingEdge, minDistance) = heads.values.min(by: { $0.1 < $1.1 })
        else {
            return nil
        }
        current = leadingEdge.target
        currentDistance = minDistance
    }
    
    return nil
}
