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
}

protocol GraphTrace {
    associatedtype Edge : GraphEdge
    func append(_ edge: Edge) -> Self
    func merge(with: Self) -> Self
}

struct NullTrace<E : GraphEdge> : GraphTrace {
    func append(_ edge: E) -> NullTrace {
        return self
    }
    func merge(with: NullTrace) -> NullTrace {
        return self
    }
}

func dijkstra<T : GraphTrace>(with getAdjacent: (T.Edge.Vertex) -> [T.Edge],
                         start: T.Edge.Vertex,
                         isEnd: (T.Edge.Vertex) -> Bool,
                         trace: T) -> (Int, T)? {
    var heads = Dictionary<T.Edge.Vertex, (Int, T)>()
    var current = start
    var currentDistance = 0
    var visited = Set<T.Edge.Vertex>()
    var currentTrace = trace
    
    func updateAdjacent(_ edge: T.Edge, trace: T) {
        let distance = currentDistance + edge.distance
        let newTrace = trace.append(edge)
        if let (storedDistance, storedTrace) = heads[edge.target] {
            if storedDistance > distance {
                heads[edge.target] = (distance, newTrace)
            } else if storedDistance == distance {
                heads[edge.target] = (distance, storedTrace.merge(with: newTrace))
            }
        } else {
            heads[edge.target] = (distance, newTrace)
        }
    }
    
    while isEnd(current) == false {
        for edge in getAdjacent(current).filter({!visited.contains($0.target)}) {
            updateAdjacent(edge, trace: currentTrace)
        }
        visited.insert(current)
        heads.removeValue(forKey: current)
        guard let (vertex, (minDistance, headTrace)) = heads.min(by: { $0.1.0 < $1.1.0 })
        else {
            return nil
        }
        current = vertex
        currentDistance = minDistance
        currentTrace = headTrace
    }
    
    return (currentDistance, currentTrace)
}

func dijkstra<E : GraphEdge>(with getAdjacent: (E.Vertex) -> [E],
                             start: E.Vertex,
                             isEnd: (E.Vertex) -> Bool) -> Int? {
    dijkstra(with: getAdjacent, start: start, isEnd: isEnd, trace: NullTrace<E>())?.0
}
